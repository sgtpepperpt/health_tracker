from django.db import models

from healthtracker.models.models import SingletonModel


class _BaseChecker(SingletonModel):
    active = models.BooleanField(verbose_name='Check status', default=False)

    class Meta:
        abstract = True

    def get_status(self, cls, value):
        pass


class RangeChecker(_BaseChecker):
    lower_danger = models.FloatField(blank=True, null=True, verbose_name='Lower danger bound')
    lower_ok = models.FloatField(blank=True, null=True, verbose_name='Lower ok bound')
    upper_ok = models.FloatField(blank=True, null=True, verbose_name='Upper ok bound')
    upper_danger = models.FloatField(blank=True, null=True, verbose_name='Upper danger bound')

    class Meta:
        abstract = True

    def get_status(self, cls, value):
        c = cls.checker.load()
        if not c.active or not (c.lower_danger and c.lower_ok and c.upper_ok and c.upper_danger):
            # TODO might accept some combinations (eg ok or danger only)
            return None

        return 'success' if c.lower_ok <= value <= c.upper_ok \
            else 'warning' if c.lower_danger <= value <= c.upper_danger \
            else 'danger'


class ListChecker(_BaseChecker):
    ok_values = models.CharField(blank=True, null=True, max_length=1024)
    warning_values = models.CharField(blank=True, null=True, max_length=1024)

    class Meta:
        abstract = True

    def get_status(self, cls, value):
        c = cls.checker.load()
        if not c.active or not c.ok_values or not c.warning_values:
            return None

        ok_list = c.ok_values.split(',')
        warning_list = c.warning_values.split(',')

        return 'success' if str(value) in ok_list \
            else 'warning' if str(value) in warning_list \
            else 'danger'
