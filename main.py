import webapp2

from app.controller import admin_controller, page_controller

config = {
  'webapp2_extras.sessions': {
    'secret_key': 'my-super-secret-key'
  }
}

app = webapp2.WSGIApplication([
  (r'/admin/(.*)', admin_controller.AdminController),
  (r'/(.*)?', page_controller.PageController)
], config=config)