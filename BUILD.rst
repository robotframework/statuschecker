Releasing StatusChecker
=======================

1. Execute tests using different Python implementations and versions.
   See `<test/README.rst>`_ for instructions.

2. Set ``$VERSION`` shell variable to ease copy-pasting further commands::

      VERSION=x.y

3. Update ``__version__`` in `<robotstatuschecker.py>`_::

      inv set-version 1.5.0
      git diff  # verify changes
      git commit -m "Updated __version__ to $VERSION" robotstatuschecker.py
      git push

4. Tag::

      git tag -a $VERSION -m "Release $VERSION" && git push --tags

5. Create distribution::

      python setup.py sdist register upload

6. Verify that `PyPI pages <https://pypi.python.org/pypi/robotstatuschecker>`_
   look good.

7. Test that installation works::

      pip install robotstatuschecker --upgrade

8. ``__version__`` back to ``devel``::

      inv set-version devel
      git diff  # verify changes
      git commit -m "__version__ back to devel" robotstatuschecker.py
      git push

9. Advertise on mailing lists, `Twitter <https://twitter.com/robotframework>`_,
   `LinkedIn <https://www.linkedin.com/groups/3710899>`_, and elsewhere as
   needed.
