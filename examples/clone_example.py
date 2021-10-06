"""clone all files"""
from pathlib import Path

from git import Repo

from github_classroom.config import assignment_from_config

assignment = assignment_from_config('config.ini')

# the folder in which to clone the repos
clone_path = Path('cloned_repos')

for identifier, github_username, repo in assignment.roster():
    if repo:
        local_path = clone_path.joinpath(repo.name)
        print(f'{identifier!r}: cloning to {local_path}')
        cloned_repo = Repo.clone_from(repo.authenticated_clone_url, local_path)
    else:
        print(f'{identifier!r} has not created a repo yet')