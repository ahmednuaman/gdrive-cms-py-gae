import config

from apiclient.discovery import build
from app.controller.base_controller import BaseController
from oauth2client.client import OAuth2WebServerFlow

class AdminController(BaseController):
  def get(self, callback):
    # set up our client
    self._set_up_client()

    # load edit view
    self._edit()

  def _edit(self, folder=None):
    # if the user has selected a folder, get its contents
    folder_contents = None

    if folder is not None:
      folder_contents = self._client.files.get(folderId=folder).execute()

    # get the root folders
    root_folders = self._client.files.get().execute()

    self.response.out.write(root_folders)

  def _set_up_client(self):
