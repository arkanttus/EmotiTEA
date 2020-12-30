from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.filter
def idx(arg1, arg2):
    print(arg1)
    print(arg2)
    return arg1[arg2]