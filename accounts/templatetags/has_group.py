# Customized template tag to check if a user has a specific group
# To be loaded in the template usng {% load has_group %}

from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()