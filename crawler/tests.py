from . import (_filter_changelog_files, _parse_changelog_text,
               _extract_version, _starts_with_ident, _parse_item)
from allmychanges.utils import transform_url
from nose.tools import eq_

def test_changelog_finder():
    in_ = [
          './release.sh',
          './docs/RELEASE_NOTES.TXT',
          './docs/releases.rst',
          './kiva/agg/freetype2/docs/release',
          './seed/commands/release.py',
          './doc/source/manual/AppReleaseNotes.rst',
          './src/robotide/application/releasenotes.py',
          './scripts/make-release.py',
          './pypi_release.sh',
          './doc/release.rst',
          './release-process.txt',
          './docs/release_notes/v0.9.15.rst',
          './release.sh',
          './.travis-release-requirements.txt',
          './mkrelease.sh',
    ]

    out = [
          './docs/RELEASE_NOTES.TXT',
          './docs/releases.rst',
          './doc/source/manual/AppReleaseNotes.rst',
          './doc/release.rst',
          './release-process.txt',
          './docs/release_notes/v0.9.15.rst',
          './.travis-release-requirements.txt',
    ]
    eq_(out, list(_filter_changelog_files(in_)))


def test_flask_parser():
    input = """
Flask Changelog
===============

Here you can see the full list of changes between each Flask release.

Version 1.0
-----------

(release date to be announced, codename to be selected)

- Added ``SESSION_REFRESH_EACH_REQUEST`` config key that controls the
  set-cookie behavior.  If set to `True` a permanent session will be
  refreshed each request and get their lifetime extended, if set to
  `False` it will only be modified if the session actually modifies.
  Non permanent sessions are not affected by this and will always
  expire if the browser window closes.

Version 0.10.2
--------------

(bugfix release, release date to be announced)

- Fixed broken `test_appcontext_signals()` test case.
- Raise an :exc:`AttributeError` in :func:`flask.helpers.find_package` with a
  useful message explaining why it is raised when a PEP 302 import hook is used
  without an `is_package()` method.

Version 0.7.1
-------------

Bugfix release, released on June 29th 2011

- Added missing future import that broke 2.5 compatibility.
- Fixed an infinite redirect issue with blueprints.
"""
    parsed = _parse_changelog_text(input)
    eq_(3, len(parsed))
    eq_('1.0', parsed[0]['version'])
    eq_('0.10.2', parsed[1]['version'])
    eq_('0.7.1', parsed[2]['version'])

    eq_(1, len(parsed[0]['sections']))
    eq_('(release date to be announced, codename to be selected)',
        parsed[0]['sections'][0]['notes'])
        
    eq_(1, len(parsed[0]['sections'][0]['items']))
    eq_(('Added ``SESSION_REFRESH_EACH_REQUEST`` config key that controls the '
         'set-cookie behavior.  If set to `True` a permanent session will be '
         'refreshed each request and get their lifetime extended, if set to '
         '`False` it will only be modified if the session actually modifies. '
         'Non permanent sessions are not affected by this and will always '
         'expire if the browser window closes.'),
        parsed[0]['sections'][0]['items'][0])

def test_extract_version():
    eq_(None, _extract_version('Just a text with some 1 33 nubers'))
    eq_('1.0', _extract_version('Version 1.0'))
    eq_('0.10.2', _extract_version('Version 0.10.2'))
    eq_(None, _extract_version('  some number in the item\'s text 0.1'))


def test_parse_item():
    eq_((False, 0, None), _parse_item('Blah minor'))
    eq_((False, 0, None), _parse_item('  Blah minor'))
    eq_((True, 2, 'Blah minor'), _parse_item('- Blah minor'))
    eq_((True, 3, 'Blah minor'), _parse_item(' - Blah minor'))
    eq_((True, 5, 'Blah minor'), _parse_item('  -  Blah minor'))
    eq_((True, 5, 'Blah minor'), _parse_item('  *  Blah minor'))

    
def test_starts_with_ident():
    eq_(False, _starts_with_ident('Blah', 0))
    eq_(False, _starts_with_ident('Blah', 1))
    eq_(False, _starts_with_ident(' Blah', 2))
    eq_(False, _starts_with_ident('  Blah', 1))
    eq_(True,  _starts_with_ident('  Blah', 2))
    eq_(True,  _starts_with_ident(' Blah', 1))
    

def test_url_normalization():
    eq_(('git@github.com:svetlyak40wt/blah', 'svetlyak40wt', 'blah'),
        transform_url('https://github.com/svetlyak40wt/blah'))
    eq_(('git@github.com:svetlyak40wt/blah', 'svetlyak40wt', 'blah'),
        transform_url('https://github.com/svetlyak40wt/blah/'))
    eq_(('git@github.com:svetlyak40wt/blah', 'svetlyak40wt', 'blah'),
        transform_url('http://github.com/svetlyak40wt/blah'))
    eq_(('git@github.com:svetlyak40wt/blah', 'svetlyak40wt', 'blah'),
        transform_url('git@github.com:svetlyak40wt/blah'))
