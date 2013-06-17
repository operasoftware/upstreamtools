#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template('upstreamed_commits.html')

print tmpl.render(name='Odin')
