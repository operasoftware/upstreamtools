#!/usr/bin/env bash

git checkout master 2> /dev/null

for p in chromium.blink chromium.src v8; do
    git --git-dir=$p.git fetch 2> /dev/null
done

python generate_upstream_list.py > upstream.html
git checkout gh-pages 2> /dev/null
mv upstream.html index.html
git commit -m "Update upstream overview." index.html
