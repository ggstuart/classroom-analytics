import requests
from collections import Counter

from .branch import Branch

class Repository:
    def __init__(self, data, auth):
        self._data = data
        self.auth = auth

    def __getattr__(self, name):
        return self._data[name]

    def __str__(self):
        return f'Repository({self.name})'

    def branches(self, **kwargs):
        response = requests.get(
            self.branches_url[:-9],
            auth=self.auth,
            params=kwargs
        )
        data = response.json()
        for d in data:
            d['commits_url'] = self.commits_url[:-6]
            yield Branch(d, self.auth)

    def all_commits_by_week(self):
        result = set()
        for branch in self.branches():
            result.update(branch.commits_by_week())
        return sorted(result)

    def all_commits(self):
        result = {}
        for branch in self.branches():
            for commit in branch.commits():
                result[commit.sha] = commit
        return result.values()

    def commit_weeks(self):
        return [c.week for c in self.all_commits()]

    def commit_count_by_week(self):
        return Counter(self.commit_weeks())