import os

import requests

session = requests.Session()

published_req = session.get('https://{}@api.github.com/repos/citra-emu/citra-nightly/releases'.format(os.getenv('GITHUB_TOKEN')))

if published_req.status_code == 200:
    published_releases = published_req.json()
else:
    exit()

failed_req = session.get('https://raw.githubusercontent.com/linux-gamers/arch-citra-nightly/master/builds_failed.txt')
failed_tags = {t.strip() for t in failed_req.text.split('\n') if t} if failed_req.status_code == 200 else set()

if published_releases[0]['tag_name'].split('nightly-')[1] in failed_tags:
    exit()

arch_rel_req = session.get('https://{}@api.github.com/repos/linux-gamers/arch-citra-nightly/releases/latest'.format(os.getenv('GITHUB_TOKEN')))

if arch_rel_req.status_code == 200:
    arch_latest_release = 'nightly-{}'.format(arch_rel_req.json()['tag_name'])
else:
    exit()

if published_releases[0]['tag_name'] == arch_latest_release:
    exit()


all_not_published = []

for r in published_releases:
    if r['tag_name'] > arch_latest_release and r['tag_name'] not in failed_tags:
        all_not_published.append(r['tag_name'])
    else:
        break

print(all_not_published[-1].split('nightly-')[1])
