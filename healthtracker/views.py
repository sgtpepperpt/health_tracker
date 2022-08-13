from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse
from django.utils import dateparse
from django.views import generic

from healthtracker.models.individual import IndividualForm, Individual
from healthtracker.models.readings import get_closest
from healthtracker.models.timestamp import TimestampForm, Timestamp
from healthtracker.readings.body import Weight, Height, BodyFat, BodyWater, BMI, MuscleMass, BoneMass
from healthtracker.utils.overview import generate_overview, generate_records
from healthtracker.utils.reading_utils import get_object, \
    reading_cls_to_form_cls, status_cls_to_form_cls, get_readings, get_derived_readings


@register.inclusion_tag('healthtracker/readings_widget.html')
def individual_data():
    return {
        'height': round(Height.objects.order_by('time__time').last().value) if Height.objects.count() > 0 else None
    }


def timestamp_readings(t):
    associated_readings = [getattr(t, f'{m.get_internal_name()}_set').all() for m in get_readings()]
    return [m.first() for m in associated_readings if m.count() > 0]


def get_interesting_timestamps(*wanted_readings):
    timestamps = []

    for t in Timestamp.objects.order_by('time').all():
        # check which readings where input at the timestamp
        available_readings = timestamp_readings(t)

        for a in available_readings:
            if type(a) in (wanted_readings or get_readings()):
                timestamps.append(t)
                break  # if we caught this timestamp no need to keep looking

    return timestamps


def order_data(used_readings):
    preferred_order = [m.get_short_name() for m in [Weight, BMI, BodyFat, BodyWater, MuscleMass, BoneMass]]
    preferred_order = [m for m in preferred_order if m in used_readings]
    for m in used_readings:
        if m not in preferred_order:
            preferred_order.append(m)
    return preferred_order


def generate_bmi():
    bmi = []
    for t in get_interesting_timestamps(Height, Weight):
        height = get_closest(Height, t.time, False)
        weight = get_closest(Weight, t.time, False)

        if not height or not weight:
            continue

        bmi.append(BMI(t, round(weight.value / (height.value / 100) ** 2, 1)))

    return bmi


class IndexView(generic.TemplateView):
    template_name = 'healthtracker/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        bmi = generate_bmi()

        # generate a time-oriented record of readings
        context['time_data'] = []
        used_readings = set()
        for t in Timestamp.objects.order_by('time').all():
            # check which readings where input at the timestamp
            available_readings = timestamp_readings(t)
            derived_readings = [m for m in bmi if m.time == t]

            # if there are no readings for this time don't do anything (e.g. like adding a line)
            if len(available_readings + derived_readings) == 0:
                continue

            line = {
                'time': t,
                'values': {}
            }

            context['time_data'].append(line)

            # add all readings to the line, including derived values where applicable
            for m in available_readings + derived_readings:
                used_readings.add(m.get_short_name())
                line['values'][m.get_short_name()] = m

        context['overview'] = generate_overview()
        context['records'] = generate_records()
        context['used_readings'] = order_data(used_readings)

        context['data'] = {
            'weight': Weight.objects.order_by('time__time').all(),
            'bodyfat': BodyFat.objects.order_by('time__time').all(),
            'musclemass': MuscleMass.objects.order_by('time__time').all(),
        }

        return context


class MultipleReadingsAdd(generic.TemplateView):
    template_name = 'healthtracker/reading_form.html'

    @classmethod
    def __generate_empty_forms(cls, post=None):
        # add forms for all readings, but do not require them in the front-end
        forms = {}
        for reading_cls in get_readings():
            form_cls = reading_cls_to_form_cls(reading_cls)

            form = form_cls(post) if post else form_cls()
            form.fields['value'].required = False

            forms[reading_cls.get_internal_name()] = (reading_cls.get_long_name(), form)

        return forms

    def get(self, request, *args, **kwargs):
        time_form = TimestampForm()

        return render(request, self.template_name, {
            'form': time_form,
            'forms': self.__generate_empty_forms(),
            'update': False
        })

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['time'] = dateparse.parse_datetime(post['time'])  # need this to accept ISO string timestamp

        # process timestamp
        time_form = TimestampForm(post)

        if not time_form.is_valid():
            return render(request, self.template_name, {
                'form': time_form,
                'forms': self.__generate_empty_forms(post),
                'update': True
            })

        fk = time_form.save()  # TODO should delete on error?

        # update post request with times
        for form_cls in [reading_cls_to_form_cls(cls) for cls in get_readings()]:
            post[f'{form_cls.__name__}-time'] = fk

        # instantiate forms with post request
        forms = {}
        for reading_cls in get_readings():
            form_cls = reading_cls_to_form_cls(reading_cls)

            param = f'{form_cls.__name__}-value'
            if param not in post or len(post[param]) == 0:
                continue

            forms[reading_cls.get_internal_name()] = (reading_cls.get_long_name(), form_cls(post))

        if not all(form[1].is_valid() for form in forms.values()):
            default_forms = self.__generate_empty_forms()  # used to return empty forms

            # recover original ordering for forms
            return_forms = {}
            for key in [reading_cls.get_internal_name() for reading_cls in get_readings()]:
                return_forms[key] = forms.get(key) or default_forms.get(key)

            return render(request, self.template_name, {
                'form': time_form,
                'forms': return_forms,
                'update': True
            })

        [form[1].save() for form in forms.values()]

        # process form cleaned data
        return HttpResponseRedirect(reverse('htracker:index'))


class MultipleReadingsUpdate(generic.TemplateView):
    """
    Update readings associated with a timestamp (including the timestamp, if wanted)
    """
    template_name = 'healthtracker/reading_form.html'

    def get(self, request, *args, **kwargs):
        # TODO
        return render(request, self.template_name, {
            'form': TimestampForm(),
            'forms': {},
            'update': True
        })

    def post(self, request, *args, **kwargs):
        # TODO

        # t = Timestamp.objects.all()
        # t = t.get(pk=65)
        # t.time += timedelta(hours=3)
        # t.save()

        return render(request, self.template_name, {
            'form': TimestampForm(),
            'forms': {},
            'update': True
        })


class MultipleReadingsDelete(generic.TemplateView):
    """
    Delete all readings associated with a timestamp
    """
    template_name = 'healthtracker/reading_form.html'

    def get(self, request, *args, **kwargs):
        timestamp = Timestamp.objects.get(pk=kwargs['pk'])

        # TODO confirmation
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        timestamp = Timestamp.objects.get(pk=kwargs['pk'])
        # TODO
        # for obj in timestamp_readings(timestamp):
        #     obj.delete()
        #
        # timestamp.delete()

        return HttpResponseRedirect(reverse('htracker:index'))


class SingleReadingUpdate(generic.TemplateView):
    """
    Update a single reading
    """
    template_name = 'healthtracker/reading_form.html'

    def get(self, request, *args, **kwargs):
        # get class and object we are editing
        cls, obj = get_object(kwargs['field'], kwargs['pk'])
        form_cls = reading_cls_to_form_cls(cls)

        return render(request, self.template_name, {
            'form': TimestampForm(instance=obj.time),
            'forms': {
                cls.get_internal_name(): (cls.get_long_name(), form_cls(instance=obj))
            },
            'update': True
        })

    def post(self, request, *args, **kwargs):
        # get class and object we are editing
        cls, obj = get_object(kwargs['field'], kwargs['pk'])
        form_cls = reading_cls_to_form_cls(cls)

        # update post request with time
        post = request.POST.copy()
        post[f'{form_cls.__name__}-time'] = obj.time

        # instantiate form with post request and object instance
        form = form_cls(post, instance=obj)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': TimestampForm(instance=obj.time),
                'forms': {
                    cls.get_internal_name(): (cls.get_long_name(), form)
                },
                'update': True
            })

        # do not save timestamp, as it may be associated with other readings
        # that we're not seeing here
        form.save()
        return HttpResponseRedirect(reverse('htracker:index'))


class SingleReadingDelete(generic.TemplateView):
    """
    Delete a reading, and its timestamp, should the latter
    only be associated with the deleted reading
    """
    template_name = 'healthtracker/reading_form.html'

    def get(self, request, *args, **kwargs):
        # get form class and object we are editing
        form_cls, obj = get_object(kwargs['field'], kwargs['pk'])
        # TODO confirmation
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # get form class and object we are editing
        form_cls, obj = get_object(kwargs['field'], kwargs['pk'])

        # TODO delete
        return HttpResponseRedirect(reverse('htracker:index'))


class IndividualFormView(generic.TemplateView):
    template_name = 'healthtracker/individual_form.html'

    @classmethod
    def __get_checker_forms(cls, post=None):
        # get all checker forms, instantiated with the post request or the checker's singleton
        checker_forms = {}
        for reading in get_readings() + get_derived_readings():
            if not hasattr(reading, 'checker'):
                continue

            checker_cls = type(reading.checker)
            checker_form_cls = status_cls_to_form_cls(checker_cls)

            if post:
                checker_forms[checker_cls.__name__] = checker_form_cls(post)
            else:
                checker_forms[checker_cls.__name__] = checker_form_cls(instance=checker_cls.load())

        return checker_forms

    def get(self, request, *args, **kwargs):
        individual_form = IndividualForm(instance=Individual.load())

        return render(request, self.template_name, {
            'form': individual_form,
            'forms': self.__get_checker_forms()
        })

    def post(self, request, *args, **kwargs):
        individual_form = IndividualForm(request.POST)

        # status forms
        checker_forms = self.__get_checker_forms(request.POST)

        if not individual_form.is_valid() or not all(form.is_valid() for form in checker_forms.values()):
            return render(request, self.template_name, {
                'form': individual_form,
                'forms': checker_forms
            })

        individual_form.save()
        [f.save() for f in checker_forms.values()]

        return HttpResponseRedirect(reverse('htracker:index'))
