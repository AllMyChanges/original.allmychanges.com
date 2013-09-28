import os


def list_files():
    """Recursivly walks through files and returns them as iterable."""
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            yield os.path.join(root, file)


predicates = [
    lambda x: 'change' in x,
    lambda x: 'news' in x,
]

def search_changelog():
    """Searches changelog-like files in the current directory."""
    files = list(list_files())
    for filename in files:
        if any(p(filename.lower()) for p in predicates):
            return filename

