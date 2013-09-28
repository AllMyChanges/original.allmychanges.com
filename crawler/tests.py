from . import _filter_changelog_files
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
