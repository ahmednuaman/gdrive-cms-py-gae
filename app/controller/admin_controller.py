import config
import json
import urllib
import webapp2

from app.controller.base_controller import BaseController
from oauth2client.appengine import OAuth2Decorator
from random import randint
from time import sleep

# set up decorator
decorator = OAuth2Decorator(
  client_id=config.client_id,
  client_secret=config.client_secret,
  scope='https://docs.googleusercontent.com/ https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email'
)

class AdminController(BaseController):
  def __init__(self):
    # set up default vars
    # recur stuff
    self._recur_counter = { }
    self._recur_limit = 3

  @decorator.oauth_required
  def dispatch(self):
    # set up our client
    self._set_up_client()

    # Dispatch the request.
    webapp2.RequestHandler.dispatch(self)

  def get(self):
    # load edit view
    self._edit()

  def _edit(self, folder=None):
    # if the user has selected a folder, get its contents
    folder_contents = None

    if folder is not None:
      folder_contents = self._make_req('https://www.googleapis.com/drive/v2/files?q=' +
        urllib.quote_plus('"%s" in parents and mimeType = "application/vnd.google-apps.document"' % folder))

    # get the root folders
    root_folders = self._make_req('https://www.googleapis.com/drive/v2/files?q=' +
      urllib.quote_plus('"root" in parents and mimeType = "application/vnd.google-apps.folder"'))

    # self.response.out.write(root_folders)

  def _increment_recur_counter(self, url):
    try:
      self._recur_counter[url]++;

    except KeyError:
      self._recur_counter[url] = 1

  def _make_req(self, url, json=True):
    # make request
    resp = self._http.request(url)

    # decode
    if json:
      resp = json.loads(resp[0])

    # check response
    if resp.status not 200:
      if not self._ok_to_recur(url):
        # too much recursion
        raise Exception('Failed to make request to URL: %s; too much recursion' % url)

      # update counter
      self._increment_recur_counter(url)

      # sleep
      sleep(.001 * randint(100, 1000))

      # recur
      return self._make_req(url, json)

    # set the body
    body = resp[1]

    # parse and return
    return json.loads(body) if json else body

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