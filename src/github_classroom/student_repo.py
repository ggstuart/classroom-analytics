import logging
from datetime import datetime, timedelta
from time import gmtime, strftime
from collections import Counter

from git import Repo
from git.remote import FetchInfo

log = logging.getLogger(__name__)

class StudentRepo(Repo):

    def pull_if_needed(self, remote="origin"):
        remote = self.remotes[remote]
        if remote.fetch()[0].flags != FetchInfo.HEAD_UPTODATE:
            log.info("pulling")
            remote.pull()
        else:
            log.debug("head up to date")

    def commit_dates(self, branch='master'):
        for commit in self.iter_commits(branch):
            yield datetime.fromtimestamp(commit.authored_date).date()

    def commit_weeks(self, branch='master'):
        for dt in self.commit_dates():
            yield dt - timedelta(days=dt.isoweekday() % 7)

    def commit_months(self, branch='master'):
        for dt in self.commit_dates():
            yield dt.replace(day=1)

    def commits_per_month(self, **kwargs):
        return dict(sorted(Counter(self.commit_months()).items()))

    def commits_per_week(self, **kwargs):
        return dict(sorted(Counter(self.commit_weeks()).items()))

    def __repr__(self):
        return f'StudentRepo({self.working_dir})'