#!/usr/bin/env python2
# coding: utf-8

import re
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

def get_commit_log(git_repo, viewvc_url, author_in_commit_body=False):
    repo = Repo(git_repo)
    log = repo.commits(config.EMAIL_GREP, search_body=author_in_commit_body)
    for commit in log[:]:
        if author_in_commit_body:
            name_match = re.search(
                '(Contributed|Patch) (from|by) [^<]*<{name_re}>'.format(name_re=config.EMAIL_RE),
                commit.body)
            if not name_match:
                review_match = re.search('R=.*{}'.format(config.EMAIL_RE), commit.body)
                if review_match:
                    # Skip stuff only reviewed
                    log.remove(commit)
                    continue
                raise Exception("Didn't find {} in commit msg ({})".format(config.EMAIL_RE, commit.body))
            commit.author = name_match.group('full_email')
            commit.stripped_author = name_match.group('name')
        else:
            name_match = re.match(config.EMAIL_RE, commit.author)
            if name_match:
                commit.stripped_author = name_match.group('name')
            else:
                commit.stripped_author = commit.author

        commit.viewvc = viewvc_url.format(rev=commit.sha)
    return log

project_logs = []
for repo in config.REPOS:
    commit_log = get_commit_log(repo['gitdir'], repo['viewvc_url'],
                                repo.get('author_in_commit_body', False))
    project_logs.append({'name': repo['name'], 'log': commit_log})

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(projects=project_logs).encode('utf-8')
