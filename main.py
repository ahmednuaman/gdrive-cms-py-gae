import webapp2

from app.controller import admin_controller, page_controller

config = {
  'webapp2_extras.sessions': {
    'secret_key': 'my-super-secret-key'
  }
}

app = webapp2.WSGIApplication([
  (admin_controller.decorator.callback_path, admin_controller.decorator.callback_handler()),
  ('/admin/', admin_controller.AdminController),
  (r'/([^\/]+)?', page_controller.PageController)
], config=config)