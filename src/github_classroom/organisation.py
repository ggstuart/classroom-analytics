import logging
import requests
from requests.utils import quote
from datetime import datetime, timedelta
from collections import Counter

from .repository import Repository

base_url = "https://api.github.com"

repo_defaults = {
    "type": "private", # student repos are private
    "per_page": 10,   # 100 is the maximum, I have 200+
    "sort": "pushed",  # ordering with most 
    "direction": "desc"# recently pushed first
}

class Organisation:
    """A remote Github Organisation"""

    def __init__(self, organisation_name, username, token):
        self.auth = (username, token)
        self.name = organisation_name
        self.url = f"{base_url}/orgs/{organisation_name}"
        self._data = self._load()

    def _load(self):
        response = requests.get(self.url, auth=self.auth)
        assert response.status_code == 200
        return response.json()

    def __getattr__(self, name):
        return self._data[name]

    def __str__(self):
        return f'Organisation({self._data["url"]})'

    def _repo_page(self, **kwargs):
        """A single request for a page of repos"""
        response = requests.get(
            self._data['repos_url'], 
            params=kwargs,
            auth=self.auth 
        )
        return response.json()

    def repos(self, **kwargs):
        """paginated repos, yielded one at a time"""
        page = 1
        kwargs_with_defaults = {}
        kwargs_with_defaults.update(repo_defaults)
        kwargs_with_defaults.update(kwargs)
        while True:
            repos = self._repo_page(page=page, **kwargs_with_defaults)
            for repo in repos:
                yield Repository(repo, self.auth)
            if not len(repos):
                break
            page += 1

    def assignments(self, name, **kwargs):
        "filtered repos, only yielding those matching the given assignment"
        for repo in self.repos(**kwargs):
            if repo.name.split('-')[0] == name:
                yield repo

    def repo(self, name):
        url = f"{base_url}/repos/{self.name}/{name}"
        response = requests.get(
            url, 
            auth=self.auth 
        )
        return Repository(response.json(), self.auth)
