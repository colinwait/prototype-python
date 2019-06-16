from django import template

register = template.Library()  # 对象名必须为register


@register.filter()
def get_item(dict, key):
    return dict.get(key)
