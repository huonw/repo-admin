Basic tools for mass-updates of certain github repo settings:

- adding contributors
- adding webhooks
- deleting webhooks based on simple filters

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
./add-webhook.py -u "http://$HOMU/github" -e '*' -t 'json' -o $USERNAME -s $HOMU_SECRET $REPOS

# highfive
./add-webhook.py -u "http://$HIGHFIVE/newpr.py" -e 'pull_request' -e 'issue_comment' -t 'form' -o $USERNAME $REPOS
```
