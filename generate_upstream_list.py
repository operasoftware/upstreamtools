#!/usr/bin/env python2
import re
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

def get_commit_log(git_repo):
    repo = Repo(git_repo)
    log = repo.commits()
    for commit in log:
        m = re.search(r'git-svn-id: ([^\s]+)', commit.body)
        if not m:
            # Found nothing!
            raise Exception("Didn't find git-svn-id in the commit body! Rev {0}"
                "".format(commit.sha))
        m2 = re.match(r'svn://svn.chromium.org/([^/]+)/[^@]*@(\d+)', m.group(1))
        if not m2:
            # Found nothing!
            raise Exception("Didn't find product and revision in the svn url! "
                "Url {0}, rev {1}.".format(m.group(1), commit.sha))
        commit.product = m2.group(1)
        commit.svn_revision = m2.group(2)
        commit.viewvc = ("http://src.chromium.org/viewvc/{prod}?revision={rev}&"
                "view=revision".format(prod=commit.product, rev=commit.svn_revision))
        commit.author_stripped = commit.author.replace('@opera.com', '')
    return log

chr_log = get_commit_log(config.CHROMIUM_GIT)
blink_log = get_commit_log(config.BLINK_GIT)

log = [
    { 'name': 'Chromium', 'log': chr_log },
    { 'name': 'Blink', 'log': blink_log },
]

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(projects=log)
