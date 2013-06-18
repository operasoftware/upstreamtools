import os
import subprocess
import datetime
import time

from collections import namedtuple


class InvalidStateError(Exception): pass

class Repo(object):
    dirty = False

    def __init__(self, gitdir, git="git"):
        self.git = git
        self.gitdir = gitdir
        if not os.path.isdir(self.gitdir):
            raise InvalidStateError("Couldn't find gitdir: {0}".format(self.gitdir))

    def _git(self, args, check=True):
        if check:
            response = subprocess.check_output(
                [self.git, '--git-dir='+self.gitdir] + args, stderr=subprocess.STDOUT)
            return response.decode('utf-8')
        return subprocess.call(
            [self.git, '--git-dir='+self.gitdir] + args, stderr=subprocess.STDOUT)

    def commits(self):
        commit_type = namedtuple("Commit", "sha author date date_relative subject body")
        raw_commits = self.get_log()
        commits = []
        for c in raw_commits:
            parts = c.split('\n', 5)
            if len(parts) == 6:
                commits.append(commit_type._make(parts))
        return commits

    def get_log(self):
        lines = self._git([
                    'log',
                    '--format=%H%n%an%n%ad%n%ar%n%B',
                    '--date=short',
                    '--author=opera.com',
                    '-z',
                    'master']).split('\0')
        return lines
