import pdb

from django import template
from menu.models import Menu, MenuItem

register = template.Library()


def build_menu_tree(menu_items):

    menu_dict = {}

    for item in menu_items:
        if item.parent_item:
            parent_id = item.parent_item.id
            if parent_id not in menu_dict:
                menu_dict[parent_id] = []
            menu_dict[parent_id].append(item)
        else:
            menu_dict[item.id] = []

    def build_tree(parent_id):
        children = menu_dict.get(parent_id, [])
        return {item: build_tree(item.id) for item in children}

    root_items = [item for item in menu_items if item.parent_item is None]
    return {item: build_tree(item.id) for item in root_items}


@register.inclusion_tag('menu/menu_tag.html')
def draw_menu(menu):
    items =  menu.menu_items.all().order_by('-parent_item')
    tree = build_menu_tree(items)
    return {
        'items': tree,
    }
