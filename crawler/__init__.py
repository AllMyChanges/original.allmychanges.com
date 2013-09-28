import os


def list_files():
    """Recursivly walks through files and returns them as iterable."""
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            yield os.path.join(root, file)


include_predicates = [
    lambda x: 'change' in x,
    lambda x: 'news' in x,
    lambda x: 'release' in x,
]


exclude_predicates = [
    lambda x: x.endswith('.sh'),
    lambda x: x.endswith('.py'),
    lambda x: x.count('/') > 4,
]


def _filter_changelog_files(filenames):
    for filename in filenames:
        if any(p(filename.lower()) for p in include_predicates) and \
                not any(p(filename.lower()) for p in exclude_predicates):
            yield filename


def search_changelog():
    """Searches changelog-like files in the current directory."""
    filenames = list(list_files())
    for filename in _filter_changelog_files(filenames):
        return filename

