import os

import requests

payload = {
    'tag_name': os.environ['TAG'],
    'target_commitish': 'master',
    'name': os.environ['TAG'],
    'draft': False,
    'prerelease': False

}
print('Submitting release: {}'.format(payload))
res = requests.post('https://api.github.com/repos/linux-gamers/arch-citra-nightly/releases',
                    json=payload,
                    headers={'Authorization': 'token {}'.format(os.environ['GITHUB_TOKEN'])})

if res.status_code not in (200, 201, 202):
    print('Bad GitHub release response: {} - {}'.format(res.status_code, res.text))
    exit(1)

print("Release '{}' successfully published to GitHub".format(os.environ['TAG']))
