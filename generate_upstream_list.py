#!/usr/bin/env python2
# coding: utf-8

import re
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

def get_commit_log(git_repo, viewvc_url, author_in_commit_body=False):
    repo = Repo(git_repo)
    log = repo.commits(config.BODY_REGEX, search_body=author_in_commit_body)

    for commit in log[:]:
        author_match = re.search(config.AUTHOR_REGEX, commit.author)
        if author_match:
            commit.stripped_author = author_match.group('name')
        else:
            body_match = re.search(config.AUTHOR_REGEX, commit.body)
            if not body_match:
                raise Exception(
                    "Unable to determine original author of commit "
                    + commit.sha)
            guessed_author = body_match.group('name')
            commit.stripped_author = guessed_author

        commit.viewvc = viewvc_url.format(rev=commit.sha)
    return log

project_logs = []
for repo in config.REPOS:
    commit_log = get_commit_log(repo['gitdir'], repo['viewvc_url'],
                                repo.get('author_in_commit_body', False))
    commit_log.sort(key=lambda x: x.date, reverse=True) # FIXME: sort by time also
    project_logs.append({'name': repo['name'], 'log': commit_log})

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(projects=project_logs).encode('utf-8')
