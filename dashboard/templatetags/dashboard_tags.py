from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using the key
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument
    Usage: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """
    Divide the value by the argument
    Usage: {{ value|divide:arg }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
