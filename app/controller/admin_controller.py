import config

from apiclient.discovery import build
from app.controller.base_controller import BaseController
from oauth2client.client import OAuth2Decorator

# set up decorator
decorator = OAuth2Decorator(
  client_id=config.client_id,
  client_secret=config.client_secret,
  scope='https://docs.googleusercontent.com/ https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email',
  redirect_uri=config.redirect_uri
)

class AdminController(BaseController):
  @decorator.oauth_required
  def dispatch(self):
    # set up our client
    self._set_up_client()

    # Dispatch the request.
    webapp2.RequestHandler.dispatch(self)

  def get(self, callback):
    # load edit view
    self._edit()

  def _edit(self, folder=None):
    # if the user has selected a folder, get its contents
    folder_contents = None

    if folder is not None:
      folder_contents = self._client.files.get(folderId=folder).execute(http=self._http)

    # get the root folders
    root_folders = self._client.files.get().execute(http=self._http)

    self.response.out.write(root_folders)

  def _set_up_client(self):
    # get http obj
    self._http = decorator.http()

    # build service
    self._client = build('drive', 'v2');