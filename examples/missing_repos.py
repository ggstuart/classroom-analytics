"""A simple usage to check which students need to be reminded to create their repos"""

from github_classroom.config import assignment_from_config

assignment = assignment_from_config('config.ini')

for student in assignment.roster_file():
    if not student["github_username"]:
        print(student["identifier"])
