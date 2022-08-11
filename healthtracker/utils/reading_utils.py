from healthtracker.readings.body import Height, Weight, BodyFat, BodyWater, MuscleMass, FitnessLevel, BoneMass, \
    BasalMetabolicRate, VisceralFatLevel, Waist, HeightForm, WeightForm, BodyFatForm, BodyWaterForm, MuscleMassForm, \
    FitnessLevelForm, BoneMassForm, BasalMetabolicRateForm, VisceralFatLevelForm, WaistForm, WeightChecker, \
    WeightCheckerForm, BodyFatChecker, BodyFatCheckerForm, BodyWaterChecker, BodyWaterCheckerForm, MuscleMassChecker, \
    MuscleMassCheckerForm, FitnessLevelChecker, FitnessLevelCheckerForm, BoneMassChecker, BoneMassCheckerForm, \
    BasalMetabolicRateChecker, BasalMetabolicRateCheckerForm, VisceralFatLevelChecker, VisceralFatLevelCheckerForm, \
    WaistChecker, WaistCheckerForm, BMI, BMIChecker, BMICheckerForm


def get_readings():
    return [Height, Weight, BodyFat, BodyWater, MuscleMass, FitnessLevel, BoneMass, BasalMetabolicRate, VisceralFatLevel, Waist]


def get_derived_readings():
    return [BMI]


def get_cls(name):
    for reading in get_readings():
        if reading.get_internal_name() == name:
            return reading


def get_object(field, key):
    # get form class and object we are editing
    cls = get_cls(field)
    obj = cls.objects.get(pk=key)

    return cls, obj


def reading_cls_to_form_cls(checker):
    return {
        Height: HeightForm,
        Weight: WeightForm,
        BodyFat: BodyFatForm,
        BodyWater: BodyWaterForm,
        MuscleMass: MuscleMassForm,
        FitnessLevel: FitnessLevelForm,
        BoneMass: BoneMassForm,
        BasalMetabolicRate: BasalMetabolicRateForm,
        VisceralFatLevel: VisceralFatLevelForm,
        Waist: WaistForm
    }[checker]


def status_cls_to_form_cls(checker):
    return {
        WeightChecker: WeightCheckerForm,
        BodyFatChecker: BodyFatCheckerForm,
        BodyWaterChecker: BodyWaterCheckerForm,
        MuscleMassChecker: MuscleMassCheckerForm,
        FitnessLevelChecker: FitnessLevelCheckerForm,
        BoneMassChecker: BoneMassCheckerForm,
        BasalMetabolicRateChecker: BasalMetabolicRateCheckerForm,
        VisceralFatLevelChecker: VisceralFatLevelCheckerForm,
        WaistChecker: WaistCheckerForm,
        BMIChecker: BMICheckerForm
    }[checker]
