import csv
from datetime import datetime
import itertools

from github_classroom import get_weeks
from github_classroom.config import org_from_config

# setup some configuration
output = 'weekly_commits.csv'
organisation = org_from_config('graeme.ini')

# get the assignments and optionally filter them for testing
assignments = organisation.assignments('assignment')
n_assignments = 5
if n_assignments:
    assignments = itertools.islice(assignments, n_assignments)

# specify date range for headers
start = datetime(2021, 5, 1).date()
weeks = get_weeks(start, 23)
# print([w.strftime("%d-%m-%Y") for w in weeks])

# open the file
with open(output, 'w') as f:
    # prepare a csv writer
    writer = csv.DictWriter(f, fieldnames=['name', *weeks], extrasaction='ignore')

    # write the data
    writer.writeheader()
    for assignment in assignments:

        # show progress
        print(assignment.name)

        # prepare a row of data
        row = dict(assignment.commit_count_by_week())
        row['name'] = assignment.name

        # write it, ignoring commits outside of the given range
        writer.writerow(row)
