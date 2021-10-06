from datetime import timedelta

def get_weeks(start, n_weeks):
    one_week = timedelta(days=7)
    return [to_week(start) + one_week * i for i in range(n_weeks)]

def to_week(d):
    return d - timedelta(days=d.isoweekday() % 7)