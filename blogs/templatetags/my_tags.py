from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter()
def my_media(val):
    if val:
        return f'/media/{val}'

    return '#'


@register.simple_tag()
def manager_groups():
    return Group.objects.get(name='manager')


@register.simple_tag()
def user_groups():
    return Group.objects.get(name='user')
