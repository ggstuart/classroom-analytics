from github_classroom.config import assignment_from_config

assignment = assignment_from_config('config.ini')

for identifier, github_username, repo in assignment.roster():
    if repo:
        print()
        print(f'{identifier!r}: {github_username}')
        commits = repo.commit_count_by_week()
        for week in sorted(list(commits)):
            print(f'\t{commits[week]} commits in the week beginning {week}')
        print()
    else:
        print(f'{identifier!r} has not created a repo yet')