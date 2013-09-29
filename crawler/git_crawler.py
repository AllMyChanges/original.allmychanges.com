# -*- coding: utf-8 -*-

from datetime import datetime
import envoy
from allmychanges.utils import cd, get_package_metadata


def git_clone(repo_path, path):
    """Clone git repo from repo_path to local path"""
    r = envoy.run('git clone {repo} {path}'.format(repo=repo_path, path=path))
    if r.status_code != 0 and r.std_err != '':
        return False
    return True


def git_log_hash(path):
    """Return list of tuples ('hash', 'date', 'commit message')"""
    splitter = '-----======!!!!!!======-----'
    ins = '--!!==!!--'
    with cd(path):
        r = envoy.run('git log --pretty=format:"%H%n{ins}%n%ai%n{ins}%n%B%n{splitter}"'.format(ins=ins, splitter=splitter))
        lst = []
        for group in r.std_out.split(splitter)[:-1]:
            _hash, date, msg = group.strip().split(ins)
            lst.append((_hash.strip(), date.strip(), msg.strip()))
        return list(reversed(lst))


def git_checkout(path, revision_hash):
    with cd(path):
        r = envoy.run('git checkout {revision}'.format(revision=revision_hash))
        if r.status_code == 0:
            return True
        return False


def aggregate_git_log(path, progress_callback=lambda progress: None):
    """Return versions and commits in standard format.
    Optional callback called from time to time while worker run though git log.
    It's argument is float from 0.0 to 1.0"""
    versions = list()

    current_version, current_commits = None, list()

    log_data = git_log_hash(path)
    log_length = len(log_data)
    progress_step = max(1, log_length / 100)
    
    for idx, (rev_hash, date, msg) in enumerate(log_data):
        if idx % progress_step == 0:
            progress_callback(float(idx) / log_length)
            
        current_commits.append(msg)
        if git_checkout(path=path, revision_hash=rev_hash):
            version = get_package_metadata(path=path, field_name='Version')
            if version != current_version:
                # memorize it
                versions.insert(0,
                                dict(version=version,
                                     date=datetime.strptime(date.rsplit(' ', 1)[0], '%Y-%m-%d %H:%M:%S'),
                                     sections=[dict(notes='',
                                                    items=list(reversed(current_commits)))]))

                current_version, current_commits = version, list()

    if current_commits:
        versions.insert(0,
                        dict(version='newest',
                             date=None,
                             sections=[dict(notes='',
                                           items=list(reversed(current_commits)))]))

    return versions
