AUTHOR_REGEX = r'(?P<name>[^@\s<]+)@opera\.com'
BODY_REGEX = r'(Contributed|Patch) (from|by).*@opera\.com'

# Must be the actual '.git'-folder, not a checkout.
REPOS = [
    {
      'name': 'Chromium',
      'gitdir': './chromium.src.git',
      'viewvc_url': 'https://chromium.googlesource.com/chromium/src/+/{rev}',
    },
    {
      'name': 'V8',
      'gitdir': './v8.git',
      'viewvc_url': 'https://github.com/v8/v8/commit/{rev}',
      'author_in_commit_body': True,
    },
]
