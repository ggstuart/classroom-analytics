import csv
from pathlib import Path

class Assignment:
    """Represents a classroom assignment"""
    def __init__(self, organisation, roster_filename, prefix):
        self.roster_path = Path(roster_filename)
        self.prefix = prefix
        self.organisation = organisation


    def _repo(self, github_username):
        repo_name = f"{self.prefix}-{github_username}"
        return self.organisation.repo(repo_name)


    def roster_file(self):
        """yield each row of the roster file"""
        with self.roster_path.open('r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def roster(self):
        for student in self.roster_file():
            identifier = student['identifier']
            github_username = student['github_username']
            if github_username:
                yield identifier, github_username, self._repo(github_username)
            else:
                yield identifier, github_username, None

