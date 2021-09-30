import os.path
import itertools
import logging
from configparser import ConfigParser
import csv

from github_classroom import GithubOrganisation

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

conf = ConfigParser()
conf.read('simon.ini')

# github credentials
username = conf.get('github', 'username')
token = conf.get('github', 'token')
organisation = conf.get('github', 'organisation')
assignment_prefix = conf.get('github', 'assignment_prefix')

# create a github organisation object with the appropriate access
org = GithubOrganisation(organisation, username, token)

repos = org.classroom_repos(assignment_prefix)

n_repos = 5
if n_repos:
    repos = itertools.islice(repos, n_repos) 

# weeks = set()
for repo in repos:
    # branches = repo.branch_names()
    # print(branches)
    # commits_by_week = repo.commits_by_week()
    # print(commits_by_week)
    # weeks.update(commits_by_week)

    # print(repo.first_branch())
    # for k in repo.first_branch():
    #     print(k)

    commits_by_week = repo.commits_by_week_all_branches()
    print(commits_by_week)
    print(sum(commits_by_week.values()))