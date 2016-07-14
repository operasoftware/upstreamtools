#!/usr/bin/env bash

#set -x  # Display commands as they are run

for p in chromium.src v8; do
    git --git-dir=$p.git fetch -q
done

python generate_upstream_list.py > upstream.html || {
    echo "Python script errored out. Quitting." 1>&2; exit 1; }

# Check that we didn't just delete the file
if [[ $(du upstream.html|cut -f 1) -lt 128 ]]; then
    echo
    echo "Upstream file less than 128 chars. Not committing." 1>&2
    exit 1
fi

git checkout -q gh-pages || {
    echo "Trouble checking out gh-pages. Quitting." 1>&2; exit 1; }
mv upstream.html index.html

git add index.html
git diff-index --quiet HEAD --
ret=$?
if [ "$ret" -eq 1 ]
then
    git commit -m "Update upstream overview." index.html > /dev/null
    if [[ $1 == 'push' ]]; then
        git push -q
        git checkout -q master
        ret=0
    else
        echo
        echo "Check it with 'git show', then push it:"
        echo
        echo "git push && git checkout master"
        exit 0
    fi
else
    echo "No changes."
fi

exit $ret
