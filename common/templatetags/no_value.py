from django import template
register = template.Library()

@register.filter
def no_value_filler(value: str or None, message='No available content.') -> str:
    return value if value else message
