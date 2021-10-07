# Github Classroom Analytics

A python tool for tracking student engagement in github classroom assignments.

Essentially it uses the classroom roster and the github API to check whether students have set up a repository and if they have, it grabs their commit data and generates basic statistics.

## Basic usage

A simple example which loops over all the students and prints out their stats.

```python
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
```

The above code generates output in the following format:

```
'student1' has not created a repo yet
'student2' has not created a repo yet
'student3' has not created a repo yet

'student4': 'myAmazingGithubName'
	1 commits in the week beginning 2021-09-26
	4 commits in the week beginning 2021-10-03
	6 commits in the week beginning 2021-10-10
	2 commits in the week beginning 2021-10-17
	35 commits in the week beginning 2021-10-24

```

See the [csv_example](examples/csv_example.py) for a more practical approach

## Configuration

The above example requires a `'config.ini'` file like this:

```ini
[github]
username = myGithubUsername
token = ghp_personal_access_token
organisation = GithubOrganisationName

[classroom]
assignment_prefix = myassignment
roster_filename = classroom_roster.csv
```

>Note that the roster file itself will need to be updated regularly to bring in new github_usernames as students accept the assignment.

## Installation

Clone the git repository, set up a virtual environment as required and run this to install the `github_classroom` library. 

```bash
pip install --editable .
```

The `--editable` flag allows for further updates to be pulled in by git.
This will be necessary whilst we are in the very early stages of development.

>Note the full stop in the above command, the command should be run in the directory where the code was cloned.