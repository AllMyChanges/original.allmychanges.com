0.2.0 (unreleased)
==================

This app is just a prototype of the idea, simple but already useful. We
already have ideas how to evolve this project into something even more
useful. Here are some directions.

 - We will add a service for authenticated users, to allow them to
   collect packages they are interested in. Then we will send a
   daily or weekly digest of all new changes in choosen packages.
 - We definitely should make a richer API, to make some useful projects
   born. One of them could be a command line tool to gather new
   changes in modules, pinned in requirements.txt
 - And of course, we are planning to broaden service's possibilities,
   expanding to other platforms and languages.

Stay tuned, subscribe to our news-letter or twitter (http://twitter.com/allmychanges)
to receive news and ealier inventations to betas.

0.1.0 (2013-09-28)
==================

This app provides an easy way to collect changelogs of different
libraries. All information is gathered and presented in one format.

There are at least two possibilities to collect changelog data.

Firstly, allmychanges.com tries to find a plaintext file with
handwriten changelog. If it was found, we parse it and put to cache.

If there is no handwritten changelog, our robot applies all
his intelligence, to extract library's versions from VCS history and
tie each commit message to particular version. This is not very
accurate approach, but it is better than nothing.

First approach works with any kind of repository be it python, ruby or
even java, whereas as second approach needs more insights what is code
about. Right now, second approach only works with python modules, whose
setup.py uses setuptools.

There are plenty directions for approvement. Stay tuned.