EMAIL_GREP = '@opera.com'
EMAIL_RE = r'(?P<full_email>(?P<name>[^@]+)@opera\.com)'

# Must be the actual '.git'-folder, not a checkout.
REPOS = [
    {
      'name': 'Chromium',
      'gitdir': './chromium.src.git',
      'viewvc_url': 'https://chromium.googlesource.com/chromium/src/+/{rev}',
    },
    {
      'name': 'Blink',
      'gitdir': './chromium.blink.git',
      'viewvc_url': 'https://chromium.googlesource.com/chromium/blink/+/{rev}',
    },
    {
      'name': 'V8',
      'gitdir': './v8.git',
      'viewvc_url': 'https://github.com/v8/v8/commit/{rev}',
      'author_in_commit_body': True,
    },
]
