import webapp2

from app.controller import
  admin_controller.AdminController as AdminController,
  page_controller.PageController as PageController

app = webapp2.WSGIApplication([
  (r'/admin/(.*)', AdminController),
  (r'/(.*)?', PageController)
])