#!/usr/bin/python3

import requests
import argparse
import sys
import os.path
import subprocess

def err(msg, *args):
    print('error:', msg % args, file = sys.stderr)

parser = argparse.ArgumentParser(description = 'add a webhook to many travis.ymls')
parser.add_argument('-u', '--url', metavar = 'URL', type=str, required=True,
                    help='URL for the webhook')
parser.add_argument('directories', nargs='*', type=str,
                    help='Directories to add to')
parser.add_argument('-g', '--git', choices=['none', 'commit', 'push'], default='none',
                    help='What to do with git (default: push)')
parser.add_argument('--allow-off-master', default=False, action='store_true',
                    help='Only interact with git if the master branch is checked out')

args = parser.parse_args()

to_insert = '''\
notifications:
    webhooks: %s
''' % args.url

def git(*args, cwd=None):
    with subprocess.Popen(['git'] + list(args),
                          cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError('git %s returned non-zero code, %s: %s'
                               % (' '.join(args),
                                  proc.returncode,
                                  err))
        return out.decode()

for dir in args.directories:
    travis = os.path.join(dir, '.travis.yml')
    try:
        with open(travis) as f:
            contents = f.read()
    except FileNotFoundError:
        err('`%s` does not contain a .travis.yml', dir)
        continue

    if args.url in contents:
        print('Skipping %s, already has hook' % dir)
    elif 'webhooks' in contents:
        err('`%s` already contains a different webhook, handle manually' % travis)
        continue
    else:
        print('Adding %s' % dir)
        with open(travis, 'w') as f:
            f.write(to_insert)

        if args.git == 'none':
            continue
        on_master = git('rev-parse', '--abbrev-ref', 'HEAD', cwd=dir).strip() == 'master'
        if not (on_master or args.allow_off_master):
            print('\tNot on `master`, skipping git interactions')
            continue
        git('add', '.travis.yml', cwd=dir)
        git('commit', '-m', 'Add %s webhook to travis' % args.url, cwd=dir)
        if args.git == 'commit':
            continue
        git('push', 'origin', 'master', cwd=dir)
