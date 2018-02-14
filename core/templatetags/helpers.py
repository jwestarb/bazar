from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def formata_valor(value):
    """
    Formata um valor em R$
    """
    return "R$ {}".format(value)