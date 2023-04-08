import datetime
import time

from django.db.models import Max
from scipy import stats

from healthtracker.models.individual import Individual
from healthtracker.readings.body import Weight
from healthtracker.utils.reading_utils import get_readings


def generate_overview():
    overview = {}

    goal_defined = Individual.load().goal

    # goal-dependent data
    if goal_defined:
        goal = Individual.load().goal

        # how much weight must change to goal
        if Weight.objects.count() > 0:
            overview['goal_delta'] = Weight.objects.order_by('time__time').last().value - goal

        # projection of progress
        if Weight.objects.count() > 1:
            weight_readings = Weight.objects.order_by('time__time').all()
            times = [time.mktime(w.time.time.timetuple()) for w in weight_readings]
            weights = [w.value for w in weight_readings]

            slope, intercept, r, p, std_err = stats.linregress(times, weights)
            end_time = (goal - intercept)/slope

            overview['projected_end'] = datetime.datetime.fromtimestamp(end_time)

    # last of each reading
    overview['last'] = {m.get_internal_name(): m.objects.order_by('time__time').last() for m in get_readings() if m.objects.count() > 0}

    return overview


def generate_records():
    records = {}

    if Weight.objects.count() > 0 and Individual.load().goal:
        wants_to_lose = Weight.objects.order_by('time__time').last().value >= Individual.load().goal
        records['weight'] = Weight.objects.order_by('value').first() if wants_to_lose else Weight.objects.order_by('value').last()

    return records
