# import requests
from . import to_week
from datetime import datetime, timedelta

fmt = "%Y-%m-%dT%H:%M:%SZ"

class Commit:
    def __init__(self, data, auth):
        self.sha = data['sha']
        self._data = data
        self.auth = auth

    def __getattr__(self, name):
        return self._data[name]

    def __str__(self):
        return f'Commit({self.sha}, {self.datetime})'

    @property
    def datetime(self):
        return datetime.strptime(self.commit["author"]["date"], fmt)

    @property
    def date(self):
        return self.datetime.date()

    @property
    def week(self):
        return to_week(self.date)

    def date_and_sha(self):
        return (
            self.date,
            self.sha, 
        )

    def week_and_sha(self):
        return (
            self.week,
            self.sha, 
        )
