from django import forms
from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    time = models.DateTimeField(default=timezone.now)


class TimestampForm(forms.ModelForm):
    class Meta:
        model = Timestamp
        fields = '__all__'
        # widgets = {
        #     'time': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S.%f%z')
        # }
