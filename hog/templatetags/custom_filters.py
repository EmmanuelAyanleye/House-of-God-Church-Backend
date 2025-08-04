from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def range_filter(value):
    try:
        return range(1, int(value) + 1)
    except (TypeError, ValueError):
        return range(0)