import jinja2

from app.helper import file_helper

def load(name, data={}):
  # set the file
  file = '%s_view.html' % name

  # set the folder
  folder = 'app/view/'

  # and the path
  path = folder + file

  # check the file exists
  if file_helper.check(path) is False:
    # gracefully default to the standard app file
    file = 'page_view.html'

  # set up env for the renderer
  env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder))

  # prepare the template
  template = env.get_template(file)

  # render and return the template
  return template.render(data)