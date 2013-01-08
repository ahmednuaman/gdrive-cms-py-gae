from google.appengine.ext import db

class PageModel(db.Model):
  g_id = db.StringProperty()
  title = db.StringProperty()
  name = db.StringProperty()
  body = db.TextProperty()
  child_of = db.StringProperty()
  is_home = db.BooleanProperty(default=False)
  is_folder = db.BooleanProperty(default=False)

def get_page(name):
  return PageModel.get_by_key_name(name) if name else PageModel.gql('WHERE is_home = :1', True).get()

def get_pages():
  return PageModel.all()

def rebuild(files):
  # empty our model
  db.delete(PageModel.all(keys_only=True))

  # loop through our files and add them to the model
  _add_files_to_model(files)

  return True

def _add_files_to_model(files, parent=None):
  # loop through files
  for file in files:
    # set our base props
    model = PageModel(key_name=file.name)

    model.g_id = file.g_id
    model.title = file.title
    model.name = file.name

    if hasattr(file, 'children'):
      # a folder
      model.is_folder = True

      model.put()

      # loop through the children
      _add_files_to_model(file.children, file.name)

    else:
      # a file
      model.is_folder = False
      model.body = file.body
      model.child_of = parent
      model.is_home = file.is_home

      model.put()