from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django import forms
from django.db import models

from healthtracker.models.models import SingletonModel


class Individual(SingletonModel):
    goal = models.FloatField(blank=True, null=True)
    goal_deadline = models.DateTimeField(blank=True, null=True)


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'individual_form'
        self.helper.layout = Layout()

        self.helper.layout.append(
            Row(
                Column('goal'),
                Column('goal_deadline')
            )
        )
        self.helper.layout.append(HTML('<hr/>'))
