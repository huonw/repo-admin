#!/usr/bin/python3

import requests
import argparse
import sys

def err(msg, *args):
    print('error:', msg % args, file = sys.stderr)

token = open('token').read().strip()

URL = 'https://api.github.com/repos/{owner}/{repo}/collaborators/{username}?access_token=' + token

parser = argparse.ArgumentParser(description = 'add user(s) as collaborators to many repos')
parser.add_argument('-u', '--user', metavar = 'USER', type=str, action='append',
                    help='GitHub users to add')
parser.add_argument('-o', '--owner', type=str, help='Owner of repos without a /')
parser.add_argument('repo', nargs='*', type=str,
                    help='Repositories to add to')

args = parser.parse_args()

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

    for user in args.user:
        print('Adding %s to %s/%s' % (user, owner, repo))
        url = URL.format(owner = owner, repo = repo, username = user)
        requests.put(url)
