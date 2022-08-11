from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError


class PrefixedForm(forms.ModelForm):
    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        new_kwargs = dict(kwargs, prefix=type(self).__name__)
        super(PrefixedForm, self).__init__(*args, **new_kwargs)


class UnlabeledForm(PrefixedForm):
    def __init__(self, *args, **kwargs):
        super(UnlabeledForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class RangeCheckerForm(PrefixedForm):
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['active']:
            # TODO might accept some combinations (eg ok or danger only)
            if cleaned_data.get(f'lower_danger') is None:
                self.add_error(f'lower_danger', ValidationError(f'Check status requires all bounds'))

            if cleaned_data.get(f'lower_ok') is None:
                self.add_error(f'lower_ok', ValidationError(f'Check status requires all bounds'))

            if cleaned_data.get(f'upper_ok') is None:
                self.add_error(f'upper_ok', ValidationError(f'Check status requires all bounds'))

            if cleaned_data.get(f'upper_danger') is None:
                self.add_error(f'upper_danger', ValidationError(f'Check status requires all bounds'))

        return cleaned_data


class ListCheckerForm(PrefixedForm):
    pass
