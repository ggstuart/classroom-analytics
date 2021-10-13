"""Assuming some repos have already been cloned, clone or pull all the repos"""

from pathlib import Path

from git import Repo

from github_classroom.config import assignment_from_config

assignment = assignment_from_config('config.ini')

# the folder in which to clone the repos
clone_path = Path('cloned_repos')

for identifier, github_username, repo in assignment.roster():
    if repo:
        local_path = clone_path.joinpath(repo.name)
        if not local_path.exists():
            print(f'{identifier!r}: cloning to {local_path}')
            cloned_repo = Repo.clone_from(repo.authenticated_clone_url, local_path)
        elif local_path.is_dir():
            print(f'{identifier!r}: pulling at {local_path}')
            existing_repo = Repo(local_path)
            for remote in existing_repo.remotes:
                remote.pull()
        else:
            print('Wait, there is a file here, this should be a directory')
    else:
        print(f'{identifier!r} has not created a repo yet')