from healthtracker.forms import RangeCheckerForm, UnlabeledForm
from healthtracker.models.checkers import RangeChecker
from healthtracker.models.readings import IntReading, FloatReading


class GlucoseChecker(RangeChecker):
    pass


class GlucoseCheckerForm(RangeCheckerForm):
    class Meta:
        model = GlucoseChecker
        fields = '__all__'


class Glucose(IntReading):
    checker = GlucoseChecker()
    unit = 'mg/dl'


class GlucoseForm(UnlabeledForm):
    class Meta:
        model = Glucose
        fields = '__all__'


########################################################################################################################
class CreatinineChecker(RangeChecker):
    pass


class CreatinineCheckerForm(RangeCheckerForm):
    class Meta:
        model = CreatinineChecker
        fields = '__all__'


class Creatinine(FloatReading):
    checker = CreatinineChecker()
    unit = 'mg/dl'


class CreatinineForm(UnlabeledForm):
    class Meta:
        model = Creatinine
        fields = '__all__'
