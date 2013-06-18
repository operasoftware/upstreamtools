Opera upstreamtools
===================

A script to create a web page tracking upstreamed code to the Chromium project
from Opera.

Getting started
---------------

Install the requirements (possibly inside a virtualenv):

    pip install -r requirements.txt

Get the required upstream repositories:

    git clone --mirror https://chromium.googlesource.com/chromium/src.git chromium.src.git
    git clone --mirror https://chromium.googlesource.com/chromium/blink.git chromium.blink.git

Generate the file:

    python generate_upstream_list.py
