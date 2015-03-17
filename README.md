Basic tools for mass-updates of certain github repo settings:

- adding collaborators
- adding GitHub webhooks
- deleting GitHub webhooks based on simple filters
- naively adding a webhook to .travis.yml files

They try to be as conservative and safe as possible, but true safety
is not guaranteed: these scripts may mangle your data if misused. They
are quite simple if one wishes to verify.

Be sure to check `-h` for options.

# Example

Adding a bot, and an instance of [homu] and [highfive] to 3 repos
owned by user `bar`.

[homu]: https://github.com/barosl/homu
[highfive]: https://github.com/nrc/highfive


```sh
BOTNAME=foo
USERNAME=bar
REPOS=baz qux quz

HOMU_SECRET=abc123def456

HOMU=example.com:1000
HIGHFIVE=example.com:1001

# set the bot collaborator
./add-collab.py -u $BOTNAME -o $USERNAME $REPOS

# homu
# github:
./add-webhook.py -u "http://$HOMU/github" -e '*' -t 'json' -o $USERNAME -s $HOMU_SECRET $REPOS
# travis:
# assumes that the repos are in ./baz, ./qux, ./quz, and that all have
# a .travis.yml file already. It will commit and push the travis.yml
# change to origin/master.
./travis-webhook.py -u "http://$HOMU/travis" --git push $REPOS

# highfive
./add-webhook.py -u "http://$HIGHFIVE/newpr.py" -e 'pull_request' -e 'issue_comment' -t 'form' -o $USERNAME $REPOS
```
