#!/usr/bin/env bash

for p in chromium.blink chromium.src v8; do
    git --git-dir=$p.git fetch
done

python generate_upstream_list.py > upstream.html
git checkout gh-pages
mv upstream.html index.html
git commit -m "Update upstream overview." index.html
