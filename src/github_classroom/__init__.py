from datetime import datetime, timedelta

from .github import GithubOrganisation
from .student_repo import StudentRepo

__all__ = [StudentRepo, GithubOrganisation]


def get_weeks(start, n_weeks):
    one_week = timedelta(days=7)
    return [to_week(start) + one_week * i for i in range(n_weeks)]

def to_week(d):
    return d - timedelta(days=d.isoweekday() % 7)