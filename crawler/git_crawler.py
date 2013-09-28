# -*- coding: utf-8 -*-

import envoy
from allmychanges.utils import cd, get_package_metadata


def git_clone(repo_path, path):
    """Clone git repo from repo_path to local path"""
    r = envoy.run('git clone {repo} {path}'.format(repo=repo_path, path=path))
    if r.status_code != 0 and r.std_err != '':
        return False
    return True


def git_log_hash(path):
    """Return list of tuples ('hash', 'commit message')"""
    splitter = '-----======!!!!!!======-----'
    with cd(path):
        r = envoy.run('git log --pretty=format:"%H%n%B%n{splitter}"'.format(splitter=splitter))
        lst = []
        for group in r.std_out.split(splitter)[:-1]:
            _hash, msg = group.strip().split('\n', 1)
            lst.append((_hash, msg))
        return reversed(lst)


def git_checkout(path, revision_hash):
    with cd(path):
        r = envoy.run('git checkout {revision}'.format(revision=revision_hash))
        if r.status_code == 0:
            return True
        return False


def aggregate_git_log(path):
    """Return dict: version -> list of commit messages"""
    versions = dict()

    history_hashes = git_log_hash(path)
    if not history_hashes:
        return versions

    current_version, current_commits = None, list()

    for rev_hash, msg in git_log_hash(path):
        current_commits.append(msg)
        if git_checkout(path=path, revision_hash=rev_hash):
            version = get_package_metadata(path=path, field_name='Version')
            if version != current_version:
                # memorize it
                versions[version] = current_commits
                current_version, current_commits = version, list()

    if current_commits:
        versions['newest'] = current_commits

    return versions
