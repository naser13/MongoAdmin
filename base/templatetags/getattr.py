from django import template

register = template.Library()


@register.filter(name='getattr')
def getattribute(value, arg):
    if "." in str(arg):
        firstarg = str(arg).split(".")[0]
        value = getattribute(value, firstarg)
        arg = ".".join(str(arg).split(".")[1:])
        return getattribute(value, arg)
    try:
        return value[arg]
    except (KeyError, TypeError):
        return '-'
