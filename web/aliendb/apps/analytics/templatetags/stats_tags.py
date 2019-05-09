from django import template
import math
import time


BILLION = math.pow(10, 9)
MILLION = math.pow(10, 6)
THOUSAND = math.pow(10, 3)

register = template.Library()


@register.filter
def percentage(value):
    return format(value, "0.2%")


@register.filter
def short_quantity(value):
    if value >= BILLION:
        return "%sB+" % format(value / BILLION, "0.2f")
    elif value >= 10 * MILLION:
        return "%sM+" % format(value / MILLION, "0.1f")
    elif value >= MILLION:
        return "%sM+" % format(value / MILLION, "0.2f")
    elif value >= 10 * THOUSAND:
        return "%sk+" % format(value / THOUSAND, "0.1f")
    elif value >= THOUSAND:
        return "%s+" % str(value - value % 100)
    elif value >= 100:
        return "%s+" % str(value - value % 100)
    elif value >= 10:
        return "%s+" % str(value - value % 10)
    return str(value)


@register.filter
def timestamp(value):
    t = time.gmtime(value)
    hour_ending = "s" if t.tm_hour > 1 else ""
    min_ending = "s" if t.tm_min > 1 else ""
    sec_ending = "s" if t.tm_sec > 1 else ""

    if t.tm_hour > 0:
        return time.strftime(
            "%-H hour{}, %-M minute{}".format(hour_ending, min_ending),
            time.gmtime(value))
    elif t.tm_min > 0:
        return time.strftime(
            "%-M minute{}, %-S second{}".format(min_ending, sec_ending),
            time.gmtime(value))
    else:
        return time.strftime(
            "%-S second{}".format(sec_ending),
            time.gmtime(value))
