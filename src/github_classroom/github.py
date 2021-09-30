"""
Get all the private repositories from an organisation using the github API
Filter the repository based on the name 
(in this case all repos are of the form 'assignment-[username]')
"""
import logging
import requests
from requests.utils import quote
from datetime import datetime, timedelta
from collections import Counter

from .student_repo import StudentRepo

log = logging.getLogger(__name__)

base_url = "https://api.github.com"

repo_defaults = {
    "type": "private", # student repos are private
    "per_page": 10,   # 100 is the maximum, I have 200+
    "sort": "pushed",  # ordering with most 
    "direction": "desc"# recently pushed first
}

fmt = "%Y-%m-%dT%H:%M:%SZ"

class GithubOrganisation:
    def __init__(self, organisation, username, token):
        self.auth = (username, token)
        self.org_url = f"{base_url}/orgs/{organisation}"

    def get_repos(self, **kwargs):
        query = "&".join([f"{k}={v}" for k, v in kwargs.items()])
        url = f"{self.org_url}/repos?{query}"
        log.debug(url)
        response = requests.get(url, auth=self.auth)
        return response.json()

    def classroom_repos(self, name, **kwargs):
        page = 1
        kwargs_with_defaults = {}
        kwargs_with_defaults.update(repo_defaults)
        kwargs_with_defaults.update(kwargs)
        while True:
            repos = self.get_repos(page=page, **kwargs_with_defaults)
            for repo_data in repos:
                if repo_data['name'].split('-')[0] == name:
                    yield GithubRepo(repo_data, self.auth)
                else:
                    log.debug(f"found unmatched repo {repo_data['name']}")
            if not len(repos):
                break
            page += 1

    def cloned_classroom_repos(self, root_path, name, **kwargs):
        for github_repo in self.classroom_repos(name, **kwargs):
            yield github_repo.pull_or_clone(root_path, *self.auth)


class GithubRepo:
    def __init__(self, data, auth):
        self._data = data
        self.auth = auth

    def __getitem__(self, name):
        return self._data[name]

    def path_on_disk(self, root_path):
        return root_path.joinpath(self._data['name'])

    def authenticated_clone_url(self, username, token):
        return f"//{username}:{token}@".join(self['clone_url'].split('//'))

    def commits(self, branch=None):
        url = self['commits_url'][:-6]
        if branch:
            url = f"{url}?sha={quote(branch)}"
        print(f"requesting {url}")
        response = requests.get(url, auth=self.auth)
        return response.json()

    def commits_sha_and_date(self, branch=None):
        return [(c['sha'], c['commit']['author']['date']) for c in self.commits(branch=branch)]

    def commit_dates_all_branches(self):
        branches = self.branch_names()
        result = set()
        for b in branches:
            result.update(self.commits_sha_and_date(branch=b))
        return [datetime.strptime(r[1], fmt).date() for r in result]

    def commit_dates(self, branch=None):
        commits = self.commits(branch=branch)
        return sorted([datetime.strptime(c['commit']['author']['date'], fmt).date() for c in commits])

    def commit_weeks(self, branch=None):
        dates = self.commit_dates(branch=branch)
        return [d - timedelta(days=d.isoweekday() % 7) for d in dates]

    def commit_weeks_all_branches(self):
        dates = self.commit_dates_all_branches()
        return [d - timedelta(days=d.isoweekday() % 7) for d in dates]

    def commits_by_week(self, branch=None):
        weeks = self.commit_weeks(branch=branch)
        return dict(sorted(Counter(weeks).items()))

    def commits_by_week_all_branches(self):
        weeks = self.commit_weeks_all_branches()
        return dict(sorted(Counter(weeks).items()))

    def branches(self):
        url = self['branches_url'][:-9]
        print(f"requesting {url}")
        response = requests.get(url, auth=self.auth)
        return response.json()

    def branch_names(self):
        return [b['name'] for b in self.branches()]

    def branch_urls(self):
        branch_names = self.branch_names()
        return [f"{self['branches_url'][:-9]}/{name}" for name in branch_names]

    def first_branch(self):
        url = f"{self.branch_urls()[0]}/commits"
        print(url)
        response = requests.get(url, auth=self.auth)
        return response.json()
   
    def pull_or_clone(self, root_path, username, token, skip_pull=False):
        log.info(self['name'])
        path = self.path_on_disk(root_path)
        if path.exists():
            log.debug(f"found existing repo {self['name']}")
            repo = StudentRepo(path)
            if not skip_pull:
                repo.pull_if_needed()
        else:
            log.info(f"repo {self['name']} not found - cloning")
            clone_url = self.authenticated_clone_url(username, token)
            repo = StudentRepo.clone_from(clone_url, path)
        repo.github = self
        return repo

    def __str__(self):
        return "\n".join(sorted([str(k) for k, v in self._data.items()]))
