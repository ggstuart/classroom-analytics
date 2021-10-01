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

    # def commits(self, branch=None):
    #     url = self['commits_url'][:-6]
    #     if branch:
    #         url = f"{url}?sha={quote(branch)}"
    #     print(f"requesting {url}")
    #     response = requests.get(url, auth=self.auth)
    #     return response.json()

    # def commits_sha_and_date(self, branch=None):
    #     return [(c['sha'], c['commit']['author']['date']) for c in self.commits(branch=branch)]

    # def commit_dates_all_branches(self):
    #     branches = self.branch_names()
    #     result = set()
    #     for b in branches:
    #         result.update(self.commits_sha_and_date(branch=b))
    #     return [datetime.strptime(r[1], fmt).date() for r in result]

    # def commit_dates(self, branch=None):
    #     commits = self.commits(branch=branch)
    #     return sorted([datetime.strptime(c['commit']['author']['date'], fmt).date() for c in commits])

    # def commit_weeks(self, branch=None):
    #     dates = self.commit_dates(branch=branch)
    #     return [d - timedelta(days=d.isoweekday() % 7) for d in dates]

    # def commit_weeks_all_branches(self):
    #     dates = self.commit_dates_all_branches()
    #     return [d - timedelta(days=d.isoweekday() % 7) for d in dates]

    # def commits_by_week(self, branch=None):
    #     weeks = self.commit_weeks(branch=branch)
    #     return dict(sorted(Counter(weeks).items()))

    # def commits_by_week_all_branches(self):
    #     weeks = self.commit_weeks_all_branches()
    #     return dict(sorted(Counter(weeks).items()))

    # def branches(self):
    #     url = self['branches_url'][:-9]
    #     print(f"requesting {url}")
    #     response = requests.get(url, auth=self.auth)
    #     return response.json()

    # def branch_names(self):
    #     return [b['name'] for b in self.branches()]

    # def branch_urls(self):
    #     branch_names = self.branch_names()
    #     return [f"{self['branches_url'][:-9]}/{name}" for name in branch_names]

    # def first_branch(self):
    #     url = f"{self.branch_urls()[0]}/commits"
    #     print(url)
    #     response = requests.get(url, auth=self.auth)
    #     return response.json()
   
    # def pull_or_clone(self, root_path, username, token, skip_pull=False):
    #     log.info(self['name'])
    #     path = self.path_on_disk(root_path)
    #     if path.exists():
    #         log.debug(f"found existing repo {self['name']}")
    #         repo = StudentRepo(path)
    #         if not skip_pull:
    #             repo.pull_if_needed()
    #     else:
    #         log.info(f"repo {self['name']} not found - cloning")
    #         clone_url = self.authenticated_clone_url(username, token)
    #         repo = StudentRepo.clone_from(clone_url, path)
    #     repo.github = self
    #     return repo

    # def __str__(self):
    #     return "\n".join(sorted([str(k) for k, v in self._data.items()]))
