from django import template

from healthtracker.readings.body import WeightDependantReading

register = template.Library()


@register.filter
def status(reading):
    if hasattr(type(reading), 'checker'):
        return type(reading).checker.get_status(reading, reading.value)

    return ''


@register.filter
def value(reading):
    return reading.value


@register.filter
def unit(reading):
    return reading.get_unit()


@register.filter
def name(reading):
    return reading.get_long_name()


@register.filter
def weight_part(reading):
    if isinstance(reading, WeightDependantReading):
        return reading.as_mass()
    return None


@register.filter
def get(dic, key):
    return dic.get(key)
