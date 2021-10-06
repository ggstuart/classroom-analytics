import csv
from pathlib import Path
from datetime import datetime

# from github_classroom import get_weeks
from github_classroom.config import assignment_from_config
from github_classroom import get_weeks

# setup some configuration
output_path = Path('weekly_commits.csv')

assignment = assignment_from_config('simon.ini')

start = datetime(2021, 10, 4).date()
weeks = get_weeks(start, 23)

defaults = {week : 0 for week in weeks}

with output_path.open('w') as f:
    writer = csv.DictWriter(f, fieldnames=['identifier', 'github_name', *weeks], extrasaction='ignore')
    writer.writeheader()

    for identifier, github_name, repo in assignment.roster():
        print(identifier)
        row = defaults.copy()
        row['identifier'] = identifier
        row['github_name'] = github_name
        if repo:
            row.update(dict(repo.commit_count_by_week()))
        writer.writerow(row)