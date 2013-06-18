#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader

import config
from repository import Repo

chr_repo = Repo(config.CHROMIUM_GIT)
chr_log = chr_repo.commits()

blink_repo = Repo(config.BLINK_GIT)
blink_log = blink_repo.commits()

log = [
    { 'name': 'Chromium', 'log': chr_log },
    { 'name': 'Blink', 'log': blink_log },
]

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')
print tmpl.render(projects=log)
