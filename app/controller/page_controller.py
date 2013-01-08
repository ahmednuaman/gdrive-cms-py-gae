from app.controller.base_controller import BaseController
from app.helper import template_helper
from app.model import page_model

class GMenuItem(object):
  def __init__(self, item):
    # set some defaults
    self.is_selected = False
    self.children = None

    self.id = item.g_id
    self.title = item.title
    self.name = item.name
    self.is_home = item.is_home
    self.is_folder = item.is_folder


class PageController(BaseController):
  def get(self, name):
    # get page according to name
    page = page_model.get_page(name)

    if not page:
      # show 404
      template = template_helper.load('404')

    else:
      # get menu items
      menu_items = self._prepare_menu_items(page.g_id, page_model.get_pages())

      # render the page
      template = template_helper.load('page', {
        'page': page,
        'menu': self._get_menu(menu_items)
      })

    self.response.out.write(template)

  def _get_menu(self, items):
    # prepare our html
    html = ''

    # check for items
    if items:
      html += '<ul>'

      for item in items:
        html += '<li><a %s title="%s" class="%s">%s</a>%s</li>' % (
          '' if item.is_folder else ('href="/%s"' % item.name),
          item.title,
          ' '.join([
            ('homepage' if item.is_home else ''),
            ('selected' if item.is_selected else '')
          ]),
          item.title,
          self._get_menu(item.children) if hasattr(item, 'children') else ''
        )

      html += '</ul>'

    return html

  def _prepare_menu_items(self, selected_page_id, pages, parent=None):
    # set our menu var
    menu_items = [ ]

    # get menu items
    for page in pages:
      # ignore children that aren't of this parent
      if page.child_of != parent:
        continue

      # create our item
      item = GMenuItem(page)

      # is this page selected?
      item.is_selected = item.id == selected_page_id

      # find children
      item.children = self._prepare_menu_items(selected_page_id, pages, item.name)

      # add to our menu
      menu_items.append(item)

    return menu_items