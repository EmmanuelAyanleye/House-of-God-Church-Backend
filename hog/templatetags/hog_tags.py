from django import template

register = template.Library()

@register.filter
def get_range(value):
    try:
        value = int(value)
        return range(1, value + 1)
    except (TypeError, ValueError):
        return range(0)