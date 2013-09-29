from django.utils.encoding import force_text
import os
import re
import string
import envoy
from lxml import html
from contextlib import contextmanager

from django.contrib.markup.templatetags import markup
from django.conf import settings


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
    try:
        yield
    finally:
        os.chdir(old_path)


def get_package_metadata(path, field_name):
    """Generates PKG-INFO and extracts given field.
    Example:
    get_package_metadata('/path/to/repo', 'Name')
    """
    with cd(path):
        response = envoy.run('python setup.py egg_info')
        for line in response.std_out.split('\n'):
            if 'PKG-INFO' in line:
                with open(line.split(None, 1)[1]) as f:
                    match = re.search(r'{0}: (.*)'.format(field_name), f.read())
                    if match is not None:
                        return match.group(1)


def transform_url(url):
    """Normalizes url to 'git@github.com:{username}/{repo}' and also
    returns username and repository's name."""
    username, repo = re.search(r'[/:](?P<username>[A-Za-z0-9-]+)/(?P<repo>[^/]*)', url).groups()
    if url.startswith('git@'):
        return url, username, repo
    return 'git@github.com:{username}/{repo}'.format(**locals()), username, repo



def download_repo(url, pull_if_exists=True):
    url, username, repo = transform_url(url)

    path = os.path.join(settings.REPO_ROOT, username, repo)

    if os.path.exists(os.path.join(path, '.failed')):
        return None

    if os.path.exists(path):
        if pull_if_exists:
            with cd(path):
                response = envoy.run('git checkout master')
                if response.status_code != 0:
                    raise RuntimeError('Bad status_code from git checkout master: {0}. Git\'s stderr: {1}'.format(
                            response.status_code, response.std_err))

                response = envoy.run('git pull')
                if response.status_code != 0:
                    raise RuntimeError('Bad status_code from git pull: {0}. Git\'s stderr: {1}'.format(
                            response.status_code, response.std_err))
    else:
        response = envoy.run('git clone {url} {path}'.format(url=url, path=path))

        if response.status_code != 0:
            os.makedirs(path)
            with open(os.path.join(path, '.failed'), 'w') as f:
                f.write('')
            raise RuntimeError('Bad status_code from git clone: {0}. Git\'s stderr: {1}'.format(
                response.status_code, response.std_err)
            )

    return path


def get_markup_type(filename):
    """Return markdown or rest or None"""
    extension = filename.rsplit('.', 1)[-1].lower()
    mapping = dict(
        markdown={'md', 'markdown', 'mdown'},
        rest={'rst', 'rest'},
    )
    for markup, possible_extensions in mapping.items():
        if extension in possible_extensions:
            return markup


def get_commit_type(commit_message):
    """Return new or fix or None"""
    commit_message = commit_message.lower()
    if commit_message.startswith('add'):
        return 'new'
    elif commit_message.startswith('new '):
        return 'new'
    elif '[new]' in commit_message:
        return 'new'
    elif commit_message.startswith('fix'):
        return 'fix'
    elif ' fixes' in commit_message:
        return 'fix'
    elif ' fixed' in commit_message:
        return 'fix'
    elif 'bugfix' in commit_message:
        return 'fix'
    elif '[fix]' in commit_message:
        return 'fix'
    return 'new'


def get_clean_text_from_html(raw_html):
    if not raw_html:
        return ''
    return html.tostring(html.fromstring(force_text(raw_html)), method='text', encoding=unicode)


def get_clean_text_from_markup_text(text, markup_type):
    raw_html = render_text_for_markup_type(text, markup_type=markup_type)
    return get_clean_text_from_html(raw_html)


def render_text_for_markup_type(text, markup_type):
    if markup_type == 'markdown':
        return render_markdown(text)
    elif markup_type == 'rest':
        return render_rest(text)
    else:
        return text


def render_markdown(text):
    if text is None:
        text = ''
    return markup.markdown(force_text(text))


def render_rest(text):
    if text is None:
        text = ''
    return markup.restructuredtext(force_text(text))
