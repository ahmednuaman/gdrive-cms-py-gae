import webapp2

from webapp2_extras import sessions

class BaseController(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self._session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self._session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self._session_store.get_session()