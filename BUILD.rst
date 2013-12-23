Releasing StatusChecker
=======================

1.  Update __version__ in *robotstatuschecker.py* to release version (remove
'-devel' suffix)
2.  Commit, push, add git tag and push tags
3.  Upload to PyPi with: ``python setup.py sdist upload``
4.  Change __version__ to 'x.x-devel', commit and push
5.  Check that page in PyPi looks good and ``pip install robotstatuschecker``
works.
6.  Send emails to: announce- and devel-lists. Tweet and add news to Confluence.
