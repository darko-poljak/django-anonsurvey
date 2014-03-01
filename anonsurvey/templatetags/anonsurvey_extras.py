from django import template


def dictget(value, arg):
    if not isinstance(value, dict):
        foo = value
    else:
        foo = value.get(str(arg))
    return foo


def asstr(value):
    return str(value)


register = template.Library()
register.filter('dictget', dictget)
register.filter('asstr', asstr)
