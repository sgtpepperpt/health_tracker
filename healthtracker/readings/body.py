from django.core.validators import MinValueValidator, MaxValueValidator

from healthtracker.forms import RangeCheckerForm, UnlabeledForm, ListCheckerForm
from healthtracker.models.checkers import RangeChecker, ListChecker
from healthtracker.models.readings import FloatReading, RateReading, IntReading, DerivedReading, \
    get_closest


class WeightRateToMass(RateReading):
    class Meta:
        abstract = True

    def as_mass(self):
        weight = get_closest(Weight, self.time.time, False)
        return round(weight.value * self.value / 100, 1) if weight else None


class WeightMassToRate(FloatReading):
    class Meta:
        abstract = True

    def as_rate(self):
        weight = get_closest(Weight, self.time.time, False)
        return round(self.value / weight.value * 100, 1) if weight else None


########################################################################################################################
class Height(IntReading):
    unit = 'cm'


class HeightForm(UnlabeledForm):
    class Meta:
        model = Height
        fields = '__all__'


########################################################################################################################
class WeightChecker(RangeChecker):
    pass


class WeightCheckerForm(RangeCheckerForm):
    class Meta:
        model = WeightChecker
        fields = '__all__'


class Weight(FloatReading):
    checker = WeightChecker()
    unit = 'kg'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_validator(MinValueValidator(10))
        self.append_validator(MaxValueValidator(1000))


class WeightForm(UnlabeledForm):
    class Meta:
        model = Weight
        fields = '__all__'


########################################################################################################################
class BodyFatChecker(RangeChecker):
    pass


class BodyFatCheckerForm(RangeCheckerForm):
    class Meta:
        model = BodyFatChecker
        fields = '__all__'


class BodyFat(WeightRateToMass):
    checker = BodyFatChecker()
    name = 'Body Fat'
    short_name = 'Fat %'


class BodyFatForm(UnlabeledForm):
    class Meta:
        model = BodyFat
        fields = '__all__'


########################################################################################################################
class BodyWaterChecker(RangeChecker):
    pass


class BodyWaterCheckerForm(RangeCheckerForm):
    class Meta:
        model = BodyWaterChecker
        fields = '__all__'


class BodyWater(WeightRateToMass):
    checker = BodyWaterChecker()
    name = 'Body Water'
    short_name = 'Water %'


class BodyWaterForm(UnlabeledForm):
    class Meta:
        model = BodyWater
        fields = '__all__'


########################################################################################################################
class MuscleMassChecker(RangeChecker):
    def get_status(self, reading):
        # status is calculated as percentage of weight
        timestamp = reading.time.time
        value = reading.value

        weight = get_closest(Weight, timestamp, False)

        return super(MuscleMassChecker, self).get_status(DerivedReading(None, value / weight.value * 100))


class MuscleMassCheckerForm(RangeCheckerForm):
    class Meta:
        model = MuscleMassChecker
        fields = '__all__'


class MuscleMass(WeightMassToRate):
    checker = MuscleMassChecker()
    name = 'Muscle mass'
    short_name = 'Muscle'
    unit = 'kg'


class MuscleMassForm(UnlabeledForm):
    class Meta:
        model = MuscleMass
        fields = '__all__'


########################################################################################################################
class FitnessLevelChecker(ListChecker):
    pass


class FitnessLevelCheckerForm(ListCheckerForm):
    class Meta:
        model = FitnessLevelChecker
        fields = '__all__'


class FitnessLevel(IntReading):
    checker = FitnessLevelChecker()
    name = 'Fitness Level'
    short_name = 'Fitness'


class FitnessLevelForm(UnlabeledForm):
    class Meta:
        model = FitnessLevel
        fields = '__all__'


########################################################################################################################
class BoneMassChecker(RangeChecker):
    pass


class BoneMassCheckerForm(RangeCheckerForm):
    class Meta:
        model = BoneMassChecker
        fields = '__all__'


class BoneMass(FloatReading):
    checker = BoneMassChecker()
    name = 'Bone Mass'
    short_name = 'Bone'
    unit = 'kg'


class BoneMassForm(UnlabeledForm):
    class Meta:
        model = BoneMass
        fields = '__all__'


########################################################################################################################
class BasalMetabolicRateChecker(RangeChecker):
    pass


class BasalMetabolicRateCheckerForm(RangeCheckerForm):
    class Meta:
        model = BasalMetabolicRateChecker
        fields = '__all__'


class BasalMetabolicRate(IntReading):
    checker = BasalMetabolicRateChecker()
    name = 'Basal Metabolic Rate'
    short_name = 'BMR'
    unit = 'kcal'


class BasalMetabolicRateForm(UnlabeledForm):
    class Meta:
        model = BasalMetabolicRate
        fields = '__all__'


########################################################################################################################
class VisceralFatLevelChecker(RangeChecker):
    pass


class VisceralFatLevelCheckerForm(RangeCheckerForm):
    class Meta:
        model = VisceralFatLevelChecker
        fields = '__all__'


class VisceralFatLevel(FloatReading):
    checker = VisceralFatLevelChecker()
    name = 'Visceral Fat Level'
    short_name = 'Visceral Fat'


class VisceralFatLevelForm(UnlabeledForm):
    class Meta:
        model = VisceralFatLevel
        fields = '__all__'


########################################################################################################################
class WaistChecker(RangeChecker):
    pass


class WaistCheckerForm(RangeCheckerForm):
    class Meta:
        model = WaistChecker
        fields = '__all__'


class Waist(FloatReading):
    checker = WaistChecker()
    unit = 'cm'


class WaistForm(UnlabeledForm):
    class Meta:
        model = Waist
        fields = '__all__'


########################################################################################################################
class BMIChecker(RangeChecker):
    pass


class BMICheckerForm(RangeCheckerForm):
    class Meta:
        model = BMIChecker
        fields = '__all__'


class BMI(DerivedReading):
    checker = BMIChecker()
    name = 'Body Mass Index'
    short_name = 'BMI'
