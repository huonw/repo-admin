#!/usr/bin/python3

import requests
import argparse
import sys

def err(msg, *args):
    print('error:', msg % args, file = sys.stderr)

token = open('token').read().strip()

URL = 'https://api.github.com/repos/{owner}/{repo}/hooks?access_token=' + token

events = [
    '*', 'commit_comment', 'create', 'delete', 'deployment', 'deployment_status', 'fork',
    'gollum', 'issue_comment', 'issues', 'member', 'membership', 'page_build', 'public',
    'pull_request_review_comment', 'pull_request', 'push', 'repository', 'release',
    'status', 'team_add', 'watch'
]

parser = argparse.ArgumentParser(description = 'add a webhook to many repos')
parser.add_argument('-u', '--url', metavar = 'URL', type=str, required=True,
                    help='URL for the webhook')
parser.add_argument('-t', '--content-type', choices=['json', 'form'], default='json',
                    help='Content-type for the webhook')
parser.add_argument('-e', '--event', choices=events, action='append', default=['push'],
                    help='Events to support')
parser.add_argument('-s', '--secret', default='', help='Secret for the webhook')
parser.add_argument('-o', '--owner', type=str, help='Owner of repos without a /')
parser.add_argument('repo', nargs='*', type=str,
                    help='Repositories to add to')

args = parser.parse_args()

hook = {
    'name': "web",
    'active': True,
    'events': args.event,
    'config': {
        'url': args.url,
        'content_type': args.content_type,
        'secret': args.secret
    }
}

for rawrepo in args.repo:
    splits = rawrepo.split('/')
    if len(splits) == 1:
        if args.owner is None:
            err('`%s` has no owner specified and there is no --owner argument', rawrepo)
            continue
        owner, repo = args.owner, rawrepo
    elif len(splits) == 2:
        owner, repo = splits
    else:
        err('`%s` is not a valid GitHub repo', rawrepo)
        continue

    print('Adding to %s/%s' % (owner, repo))
    url = URL.format(owner = owner, repo = repo)
    requests.post(url, json = hook)
