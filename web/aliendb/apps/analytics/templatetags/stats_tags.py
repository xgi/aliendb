from django import template
import math


BILLION = math.pow(10, 9)
MILLION = math.pow(10, 6)
THOUSAND = math.pow(10, 3)

register = template.Library()


@register.filter
def percentage(value):
    return format(value, "0.2%")


@register.filter
def short_quantity(value):
    result = ""
    if value >= BILLION:
        result = "%sB+" % format(value / BILLION, "0.2f")
    elif value >= 10 * MILLION:
        result = "%sM+" % format(value / MILLION, "0.1f")
    elif value >= MILLION:
        result = "%sM+" % format(value / MILLION, "0.2f")
    elif value >= 10 * THOUSAND:
        result = "%sk+" % format(value / THOUSAND, "0.1f")
    elif value >= THOUSAND:
        result = "%s+" % str(value - value % 100)
    elif value >= 100:
        result = "%s+" % str(value - value % 100)
    elif value >= 10:
        result = "%s+" % str(value - value % 10)
    else:
        result = str(value)
    return result
