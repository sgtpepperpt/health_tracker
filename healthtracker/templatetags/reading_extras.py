from django import template

from healthtracker.readings.body import WeightRateToMass, WeightMassToRate

register = template.Library()


@register.filter
def status(reading):
    if hasattr(type(reading), 'checker'):
        return type(reading).checker.get_status(reading)

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
def mass_part(reading):
    if isinstance(reading, WeightRateToMass):
        return reading.as_mass()
    return None


@register.filter
def rate_part(reading):
    if isinstance(reading, WeightMassToRate):
        return reading.as_rate()
    return None


@register.filter
def get(dic, key):
    return dic.get(key)
