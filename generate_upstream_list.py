#!/usr/bin/env python2
# coding: utf-8

import re
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

def get_commit_log(git_repo):
    is_v8 = 'v8' in git_repo
    repo = Repo(git_repo)
    log = repo.commits(is_v8)
    for commit in log:
        m = re.search(r'git-svn-id: ([^\s]+)', commit.body)
        if not m:
            # Found nothing!
            raise Exception("Didn't find git-svn-id in the commit body! Rev {0}"
                "".format(commit.sha))
        id = m.group(1)
        if is_v8:
            # e.g. https://v8.googlecode.com/svn/branches/bleeding_edge@18761
            m2 = re.match(r'https://v8.googlecode.com/svn/([^/]+)/[^@]*@(\d+)', id)
            m3 = re.search('(Contributed|Patch) (from|by) [^<]*<(?P<name>[^@]+)@opera\.com>',
                           commit.body)
            if not m3:
                review_match = re.search('R=[^\n]+@opera.com', commit.body)
                if review_match:
                    # Skip stuff only reviewed
                    continue
                raise Exception("Didn't find Opera employee in commit msg ({})".format(commit.body))
            author = m3.group('name')
        else:
            # e.g. svn://svn.chromium.org/blink/trunk@165617
            m2 = re.match(r'svn://svn.chromium.org/([^/]+)/[^@]*@(\d+)', id)
            author = commit.author.replace('@opera.com', '')
        if not m2:
            # Found nothing!
            raise Exception("Didn't find product and revision in the svn URL! "
                "URL {0}, rev {1}.".format(id, commit.sha))
        commit.product = m2.group(1)
        commit.svn_revision = m2.group(2)
        if is_v8:
            commit.viewvc = (
                "https://code.google.com/p/v8/source/detail?r={rev}"
                .format(rev=commit.svn_revision)
            )
        else:
            commit.viewvc = (
                "http://src.chromium.org/viewvc/{prod}?revision={rev}&"
                "view=revision"
                .format(prod=commit.product, rev=commit.svn_revision)
            )

        commit.author_stripped = author
    return log

chr_log = get_commit_log(config.CHROMIUM_GIT)
blink_log = get_commit_log(config.BLINK_GIT)
v8_log = get_commit_log(config.V8_GIT)

log = [
    { 'name': 'Chromium', 'log': chr_log },
    { 'name': 'Blink', 'log': blink_log },
    { 'name': 'V8', 'log': v8_log },
]

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(projects=log).encode('utf-8')
