#!/usr/bin/env python

"""AllMyChanges command line interface.

Depends on requests, docopt and anyjson.

Usage:
  mychanges.py <url>...
  mychanges.py -h | --help
  mychanges.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import requests
import textwrap
import anyjson

from docopt import docopt


def get_changes(url):
    response = requests.post('http://allmychanges.com/v1/repos/create-changelog/?format=json',
                             data=anyjson.serialize(dict(url=url)),
                             headers={'Content-Type': 'application/json'})
    assert response.status_code == 200, response.content
    data = anyjson.deserialize(response.content)
    repo_id = data['id']

    response = requests.get('http://allmychanges.com/v1/repos/{repo_id}/'.format(**locals()))
    assert response.status_code == 200, response.content
    data = anyjson.deserialize(response.content)
    return data['versions']


def print_changes(changes, indent=0):
    wrapper = textwrap.TextWrapper(initial_indent=' ' * (indent + 1))
    
    for version in changes:
        print '\n', ' ' * indent, u'{0} ({1})'.format(version['name'], version['date'])
        for item in version['items']:
            text = wrapper.fill(item['text'])
            if text:
                print text
                
            for line in item['changes']:
                print ' ' * (indent + 2), '*', line['text']
    

if __name__ == '__main__':
    arguments = docopt(__doc__, version='AllMyChanges CLI 0.1')

    for url in arguments['<url>']:
        changes = get_changes(url)
        if changes:
            print url
            print_changes(changes, indent=1)
