from django.db import models

from healthtracker.models.models import SingletonModel


class _BaseChecker(SingletonModel):
    active = models.BooleanField(verbose_name='Check status', default=False)

    class Meta:
        abstract = True

    def get_status(self, reading):
        pass


class RangeChecker(_BaseChecker):
    lower_danger = models.FloatField(blank=True, null=True, verbose_name='Lower danger bound')
    lower_ok = models.FloatField(blank=True, null=True, verbose_name='Lower ok bound')
    upper_ok = models.FloatField(blank=True, null=True, verbose_name='Upper ok bound')
    upper_danger = models.FloatField(blank=True, null=True, verbose_name='Upper danger bound')

    class Meta:
        abstract = True

    def get_status(self, reading):
        checker = self.load()
        if not checker.active or not (checker.lower_danger and checker.lower_ok and checker.upper_ok and checker.upper_danger):
            # TODO might accept some combinations (eg ok or danger only)
            return None

        value = reading.value

        return 'success' if checker.lower_ok <= value <= checker.upper_ok \
            else 'warning' if checker.lower_danger <= value <= checker.upper_danger \
            else 'danger'


class ListChecker(_BaseChecker):
    ok_values = models.CharField(blank=True, null=True, max_length=1024)
    warning_values = models.CharField(blank=True, null=True, max_length=1024)

    class Meta:
        abstract = True

    def get_status(self, reading):
        checker = self.load()
        if not checker.active or not checker.ok_values or not checker.warning_values:
            return None

        ok_list = checker.ok_values.split(',')
        warning_list = checker.warning_values.split(',')

        value = reading.value

        return 'success' if str(value) in ok_list \
            else 'warning' if str(value) in warning_list \
            else 'danger'
