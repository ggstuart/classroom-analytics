import requests

from .commit import Commit

class Branch:
    def __init__(self, data, auth):
        self._data = data
        self.auth = auth

    def __getattr__(self, name):
        return self._data[name]

    def __str__(self):
        return f'Branch({self.name})'

    def commits(self):
        response = requests.get(
            self.commits_url, 
            auth=self.auth,
            params={'sha': self.name}
        )
        for c in response.json():
            yield Commit(c, self.auth)

    def commits_by_week(self):
        for c in self.commits():
            yield c.week_and_sha()