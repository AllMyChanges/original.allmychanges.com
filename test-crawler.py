#!/usr/bin/env python

import os
import string
import requests
import re
import envoy


from crawler import search_changelog
from contextlib import contextmanager


def load_data(filename):
    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(
                tuple(map(string.strip, line.split(';', 1))))

    return data

@contextmanager
def cd(path):
    """Usage:

    with cd(to_some_dir):
        envoy.run('task do')
    """
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


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
                    return True
    finally:
        pass

        
def transform_url(url):
    username, repo = re.search(r'/(?P<username>[A-Za-z0-9-]+)/(?P<repo>.*)', url).groups()
    return 'git@github.com:{username}/{repo}'.format(**locals()), username, repo
    



def test():
    root = os.path.join(os.path.abspath('./'), 'data')
    reps = load_data(os.path.join(root, 'reps.csv'))

    with cd(root):
        changelogs_found = 0
        for name, url in reps:
            try:
                changelog_found = test_crawler_on(url)
                if changelog_found:
                    changelogs_found += 1

            except RuntimeError:
                pass

    print 'Changelogs found:', changelogs_found

    with open('.stats', 'w') as f:
        f.write('crawler.changelogs-found {0}\n'.format(changelogs_found))
        f.write('crawler.changelogs-parsed 0\n')
        f.write('crawler.changelog-versions-parsed 0\n')


if __name__ == '__main__':
    test()
