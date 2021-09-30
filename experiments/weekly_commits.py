import logging
import csv
from datetime import timedelta
from pathlib import Path
from configparser import ConfigParser
import itertools

from github_classroom import GithubOrganisation

# logging configuration
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# get configuration data
conf = ConfigParser()
conf.read('graeme.ini')
root_path = Path(conf.get('example', 'root_folder'))
weekly_output_file_path = root_path.joinpath(conf.get('example', 'weekly_output_file_path'))
username = conf.get('github', 'username')
token = conf.get('github', 'token')
organisation = conf.get('github', 'organisation')
assignment_prefix = conf.get('github', 'assignment_prefix')

# Make the directory we will be using if it doesn't already exist
root_path.mkdir(exist_ok=True)

# create a github organisation object with the appropriate access
org = GithubOrganisation(organisation, username, token)

# arguments we will pass to the request to github (for a list of repos)
kwargs = {
    "type": "private", # student repos are private
    "per_page": 10,    # 100 is the maximum, I have 200+
    "sort": "pushed",  # ordering with most 
    "direction": "desc"# recently pushed first
}

# this outputs a generator that will:
#  look for repos on disk
#  clone them if it doesn't find them
#  pull them if it does (unless skip_pull=True)
repos = org.cloned_classroom_repos(root_path, assignment_prefix, skip_pull=True, **kwargs)

# for testing, we can restrict the generator to the first n_repos only
# set this to zero to do all the repos
n_repos = 5
if n_repos:
    repos = itertools.islice(repos, n_repos) 


# create a set of the dates we need to cover
weeks = set()

# this actually pulls them all and extracts the data
data = {}
for repo in repos:
    count = repo.commits_per_week()
    data[repo.github['name']] = count
    weeks.update(count)

# work out the field names based on the range of dates covered by commits
first_week = min(weeks)
last_week = max(weeks)
one_week = timedelta(days=7)
n_weeks = int((last_week - first_week).days / 7) + 1
all_weeks = [first_week + one_week*i for i in range(n_weeks)]

with open(weekly_output_file_path, "w") as f:
    writer = csv.DictWriter(f, fieldnames=["name", *all_weeks])
    writer.writeheader()
    for r in data:
        row = data[r]
        row['name'] = r
        writer.writerow(row)
