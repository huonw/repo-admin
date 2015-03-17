#!/usr/bin/python3

import requests
import argparse
import sys

def err(msg, *args):
    print('error:', msg % args, file = sys.stderr)

token = open('token').read().strip()

LIST_URL = 'https://api.github.com/repos/{owner}/{repo}/hooks?access_token=' + token
DELETE_URL = 'https://api.github.com/repos/{owner}/{repo}/hooks/{id}?access_token=' + token

parser = argparse.ArgumentParser(description = 'delete a webhook matching certain parameters from many repos')

parser.add_argument('-u', '--url', metavar = 'URL', type=str, required=True,
                    help='URL for the webhook')
parser.add_argument('-s', '--secret', type=int, choices=[0,1], help='Whether the webhook has a secret')
parser.add_argument('-o', '--owner', type=str, help='Owner of repos without a /')
parser.add_argument('repo', nargs='*', type=str,
                    help='Repositories to add to')

args = parser.parse_args()

def filter(config):
    if args.secret is not None:
        has_secret = 'secret' in config
        should_have_secret = bool(args.secret)
        secret_satisfied = has_secret == should_have_secret
    else:
        secret_satisfied = True
    return config['url'] == args.url and secret_satisfied



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

    print('Deleting from %s/%s' % (owner, repo))
    list_url = LIST_URL.format(owner = owner, repo = repo)
    hooks = requests.get(list_url).json()
    print('\tFound %s hooks' % len(hooks))
    for hook in hooks:
        if hook['name'] == 'web' and filter(hook['config']):
            print('\tDeleting %s: %s' % (hook['id'], hook['config']))
            delete_url = DELETE_URL.format(owner = owner, repo = repo, id = hook['id'])
            requests.delete(delete_url)
