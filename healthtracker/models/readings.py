from typing import Type

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from healthtracker.models.timestamp import Timestamp


class _BaseReading:
    name = None
    short_name = None
    unit = ''

    @classmethod
    def get_internal_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_long_name(cls):
        return cls.name or cls.__name__

    @classmethod
    def get_short_name(cls):
        return cls.short_name or cls.get_long_name()

    @classmethod
    def get_unit(cls):
        return cls.unit


class _BaseReadingModel(_BaseReading, models.Model):
    time = models.ForeignKey(Timestamp, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __get_fields_dict(self):
        return dict((field.name, field) for field in self._meta.fields)

    def append_validator(self, validator):
        text_field = self.__get_fields_dict()['value']
        text_field.validators.append(validator)


class DerivedReading(_BaseReading):
    def __init__(self, time, value):
        self.time: Timestamp = time
        self.value = value


class IntReading(_BaseReadingModel):
    value = models.IntegerField()

    class Meta:
        abstract = True


class FloatReading(_BaseReadingModel):
    value = models.FloatField()

    class Meta:
        abstract = True


class RateReading(FloatReading):
    unit = '%'

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_validator(MinValueValidator(0))
        self.append_validator(MaxValueValidator(100))


def get_closest(cls: Type[_BaseReadingModel], time, lookahead):
    for o in cls.objects.order_by('-time__time'):
        if o.time.time <= time:
            return o

    if lookahead:
        for o in cls.objects.order_by('time__time'):
            if o.time.time >= time:
                return o

    return None
