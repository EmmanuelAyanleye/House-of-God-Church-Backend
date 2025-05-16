from django import template

register = template.Library()

@register.filter
def range_filter(value, start=1):
    try:
        return range(start, int(value) + 1)
    except (TypeError, ValueError):
        return []