import config
import json
import re
import urllib
import webapp2

from app.controller.base_controller import BaseController
from app.helper import template_helper
from app.model import page_model
from bs4 import BeautifulSoup
from oauth2client.appengine import OAuth2Decorator
from random import randint
from time import sleep

# set up decorator
decorator = OAuth2Decorator(
  client_id=config.client_id,
  client_secret=config.client_secret,
  scope='https://docs.googleusercontent.com/ https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email'
)

# our item classes
class BaseGItem(object):
  def __init__(self, item):
    self.g_id = item['id']
    self.title = item['title']
    self.name = re.sub(r'[^\w\d]+', '_', item['title'].lower())


class GFolder(BaseGItem):
  def __init__(self, item):
    BaseGItem.__init__(self, item)

    self.children = None


class GFile(BaseGItem):
  def __init__(self, item, home_file_id):
    BaseGItem.__init__(self, item)

    self.body = ''
    self.is_home = True if item['id'] == home_file_id else False


class AdminController(BaseController):
  @decorator.oauth_required
  def dispatch(self):
    # set up default vars
    # recur stuff
    self._recur_counter = { }
    self._recur_limit = 3

    # set up our client
    self._set_up_client()

    # super
    BaseController.dispatch(self)

  def get(self):
    # load edit view
    self._edit()

  def post(self):
    # load the edit view with the posted folder
    self._edit(
      self.request.get('folder'),
      self.request.get('file')
    )

  def _edit(self, folder=None, file=None):
    # set some vars
    files = None
    success = None

    # check for folder
    if folder:
      # check for the homepage file
      if file:
        # update the site
        success = self._update(folder, file)

      # get files in the folder
      files = self._make_req('https://www.googleapis.com/drive/v2/files?q=' +
        urllib.quote_plus('"%s" in parents and mimeType = "application/vnd.google-apps.document"' % folder))['items']

    # get the root folders
    folders = self._make_req('https://www.googleapis.com/drive/v2/files?q=' +
      urllib.quote_plus('"root" in parents and mimeType = "application/vnd.google-apps.folder"'))['items']

    # load the view
    template = template_helper.load('admin', {
      'folders': folders,
      'files': files,
      'success': success,
      'self_url': self.request.uri
    })

    self.response.out.write(template)

  def _get_document_contents(self, url):
    # make the request
    html = self._make_req(url, False)

    # prepare el dom
    doc = BeautifulSoup(html)

    # get the body
    body = doc.body.prettify()

    # remove body tags
    body = re.sub(r'\<\/?body[^\>]+\>', '', body)

    return body

  def _increment_recur_counter(self, url):
    try:
      self._recur_counter[url] += 1;

    except KeyError:
      self._recur_counter[url] = 1

  def _iterate_over_files(self, folder_id, home_file_id):
    # prepare vars
    files = [ ]

    # get folder contents
    items = self._make_req('https://www.googleapis.com/drive/v2/files?q=' +
      urllib.quote_plus('"%s" in parents' % folder_id))['items']

    # iterate
    for item in items:
      # is this a folder or doc?
      if item['mimeType'] == 'application/vnd.google-apps.folder':
        folder = GFolder(item)

        folder.children = self._iterate_over_files(item['id'], home_file_id)

        files.append(folder)

      elif item['mimeType'] == 'application/vnd.google-apps.document':
        file = GFile(item, home_file_id)

        file.body = self._get_document_contents(item['exportLinks']['text/html'])

        files.append(file)

    return files

  def _make_req(self, url, parse_json=True):
    # make request
    resp, body = self._http.request(url)

    # check response
    if resp.status is not 200:
      if not self._ok_to_recur(url):
        # too much recursion
        raise Exception('Failed to make request to URL: %s; too much recursion' % url)

      # update counter
      self._increment_recur_counter(url)

      # sleep
      sleep(.001 * randint(100, 1000))

      # recur
      return self._make_req(url, parse_json)

    # parse and return
    return json.loads(body) if parse_json else body

  def _ok_to_recur(self, url):
    try:
      self._recur_counter[url];

    except KeyError:
      return True

    else:
      return True if self._recur_counter[url] > self._recur_limit else False

  def _set_up_client(self):
    # get http obj
    self._http = decorator.http()

  def _update(self, folder_id, home_file_id):
    # iterate over files and folders and create el hash
    files = self._iterate_over_files(folder_id, home_file_id)

    # use our model to rebuild our pages
    return page_model.rebuild(files)