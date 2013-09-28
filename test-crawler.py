#!/usr/bin/env python

import os
import requests
import re
import envoy


from crawler import search_changelog, _parse_changelog_text
from allmychanges.utils import cd, load_data



def test_crawler_on(url):
    try:
        if False:
            result = requests.get(url)
            if result.status_code != 200:
                raise RuntimeError('Bad status code: {0}'.format(result.status_code))

        url, username, repo = transform_url(url)
        path = '{username}/{repo}'.format(
            username=username, repo=repo)

        if False:
            if os.path.exists(path):
                with cd(path):
                    result = envoy.run('git pull'.format(path=path))
            else:
                result = envoy.run('git clone {url} {path}'.format(url=url, path=path))

            if result.status_code != 0:
                raise RuntimeError('Bad status_code from git clone: {0}'.format(result.status_code))

        if os.path.exists(path):
            with cd(path):
                changelog_filename = search_changelog()
                if changelog_filename:
                    fullfilename = os.path.normpath(
                        os.path.join(os.getcwd(), changelog_filename))
                    was_parsed = False
                    num_versions = num_items = 0
                    try:
                        with open(fullfilename) as f:
                            changes = _parse_changelog_text(f.read())
                            num_versions = len(changes)
                            num_items = sum(len(section['items'])
                                            for version in changes
                                            for section in version['sections'])

                            if num_versions > 0 and num_items > 0:
                                was_parsed = True
                    except Exception:
                        pass
                    return fullfilename, was_parsed, num_versions, num_items
    finally:
        pass

    return None, False, 0, 0

        
def transform_url(url):
    username, repo = re.search(r'/(?P<username>[A-Za-z0-9-]+)/(?P<repo>.*)', url).groups()
    return 'git@github.com:{username}/{repo}'.format(**locals()), username, repo
    



def test():
    root = os.path.join(os.path.abspath('./'), 'data')
    reps = load_data(os.path.join(root, 'reps.csv'))

    with cd(root):
        changelogs_found = 0
        changelogs_parsed = 0
        changelogs_versions = 0
        changelogs_items = 0
        
        for name, url in reps:
            try:
                changelog_filename, was_parsed, num_versions, num_items = test_crawler_on(url)
                if changelog_filename:
                    changelogs_found += 1
                    if was_parsed:
                        changelogs_parsed += 1
                        changelogs_versions += num_versions
                        changelogs_items += num_items
                    print changelog_filename

            except RuntimeError:
                pass

    stats = {}
    stats['crawler.changelogs-found'] = changelogs_found
    stats['crawler.changelogs-parsed'] = changelogs_parsed
    stats['crawler.changelog-versions-parsed'] = changelogs_versions
    stats['crawler.changelog-items-parsed'] = changelogs_items

    with open('.stats', 'w') as f:
        for key, value in stats.items():
            f.write('{key} {value}\n'.format(key=key, value=value))


if __name__ == '__main__':
    test()
