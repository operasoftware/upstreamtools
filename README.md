Opera upstreamtools
===================

A script to create [a web page](http://operasoftware.github.io/upstreamtools/) tracking
upstreamed code to the Chromium project from Opera.

Getting started
---------------

Get the source:

    git clone https://github.com/operasoftware/upstreamtools
    cd upstreamtools

Install the requirements (possibly inside a virtualenv):

    pip install -r requirements.txt

Get the required upstream repositories:

    git clone --mirror https://chromium.googlesource.com/chromium/src.git chromium.src.git
    git clone --mirror https://chromium.googlesource.com/chromium/blink.git chromium.blink.git
    git clone --mirror https://github.com/v8/v8.git v8.git

Generate the file:

    python generate_upstream_list.py > upstream.html

Updating the overview
---------------------

Update the Git checkouts.

    for p in chromium.blink chromium.src v8; do git --git-dir=$p.git fetch; done

Generate the file, switch branch and check in there.

    python generate_upstream_list.py > upstream.html
    git checkout gh-pages
    mv upstream.html index.html
    git commit -m "Update upstream overview." index.html

NOTE: It should normally only add new entries. Check if it does something else.
If you did not clone the upstreames like mirrors, the master branch won't
always be poining at the newest point in history. You will have to do a `git
pull` or similar in your working directory.

License
-------

Copyright 2014 Opera Software

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
