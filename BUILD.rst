Releasing StatusChecker
=======================

1. Set ``$VERSION`` shell variable to ease copy-pasting further commands::

    $VERSION=x.y

2. Update ``__version__`` in `<robotstatuschecker.py>`__::

    sed -i "s/__version__ = .*/__version__ = '$VERSION'/" robotstatuschecker.py
    git diff  # verify changes
    git commit -am "Updated __version__ to $VERSION" && git push

3. Tag::

    git tag -a $VERSION -m "Release $VERSION" && git push --tags

4. Create distribution::

    python setup.py sdist register upload

5. Verify that `PyPI <https://pypi.python.org/pypi/robotstatuschecker>`__
   looks good.

6. Test that installation works::

    pip install robotstatuschecker --upgrade

7. ``__version__`` back to devel::

    sed -i "s/__version__ = .*/__version__ = 'devel'/" robotstatuschecker.py
    git commit -am "__version__ back to devel" && git push

8. Advertise on `Twitter <https://twitter.com/robotframework>`__ and on mailing
   lists as needed.
