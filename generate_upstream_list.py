#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

repo = Repo(config.CHROMIUM_GIT)
log = repo.commits()

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(commits=log)
