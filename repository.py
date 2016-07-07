import os
import subprocess


class InvalidStateError(Exception):
    pass


class Repo(object):
    dirty = False

    def __init__(self, gitdir, git="git"):
        self.git = git
        self.gitdir = gitdir
        if not os.path.isdir(self.gitdir):
            raise InvalidStateError("Couldn't find gitdir: {0}".format(self.gitdir))

    def _git(self, args, check=True, input=None):
        if input:
            inp = subprocess.PIPE
        else:
            inp = None
        cmd = [self.git, '--git-dir='+self.gitdir] + args
        p = subprocess.Popen(cmd,
            stdin=inp,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if input:
            stdout, stderr = p.communicate(input)
        else:
            stdout, stderr = p.communicate()

        return p.returncode, stdout, stderr

    def commits(self, search, search_body=False):
        raw_commits = self.get_log(search, search_body)
        commits = []
        for c in raw_commits:
            parts = c.split('\n', 5)
            if len(parts) == 6:
                commit = Commit(*parts)
                commits.append(commit)
        return commits

    def get_log(self, search, search_body):
        commits = []

        # Before v8 had a commit queue, upstreamed changes were landed by
        # project members, with a commit message that referred to the patch
        # author.  AFAIK git log does not provide a way to filter by
        # "--author=@opera.com OR --grep=@opera.com" so we need to run git log
        # twice then concatenate and sort the results.

        if search_body:
            # commits with a message body that mentions the author
            cmd = [ 'log', '--format=%H%n%an%n%ad%n%ar%n%B',
                    '--extended-regexp', '--date=short', '-z',
                    '--grep={search}'.format(search=search), 'master']
            _rv, bcommits, _stderr = self._git(cmd)
            commits += bcommits.decode('utf-8').strip('\0').split('\0')
            num_commits = str(len(commits))

        # commits with an @opera.com author
        cmd = [ 'log', '--format=%H%n%ae%n%ad%n%ar%n%B',
                '--author=@opera.com', '--date=short', '-z', 'master' ]
        _rv, acommits, _stderr = self._git(cmd)
        commits += acommits.decode('utf-8').strip('\0').split('\0')

        return commits


class Commit(object):
    def __init__(self, sha, author, date, date_relative, subject, body):
        self.sha = sha
        self.author = author
        self.date = date
        self.date_relative = date_relative
        self.subject = subject
        self.body = body
