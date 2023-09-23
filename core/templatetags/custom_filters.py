from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='mark_safe')
def mark_safe_as_filter(value):
    print(value)
    return mark_safe(value)


@register.filter(name='capital')
@stringfilter
def capital(value, arg):
    print(arg)
    return value[0].upper() + value[1: len(value)]