Releasing StatusChecker
=======================


Using Invoke
~~~~~~~~~~~~

Invoke tasks are defined in the `<tasks.py>`_ file and they are executed from
the command line like::

    inv[oke] task [options]

Run ``invoke`` without arguments for help. All tasks can be listed using
``invoke --list`` and each task's usage with ``invoke --help task``.

Preparation
-----------

1. Check that you are on the master branch and have nothing left to commit,
   pull, or push::

      git branch
      git status
      git pull --rebase
      git push

2. Clean up::

      invoke clean

3. Execute tests using different Python implementations and versions.
   See `<README.rst>`_ for instructions.

4. Set version information to a shell variable to ease copy-pasting further
   commands. Add ``aN``, ``bN`` or ``rcN`` postfix if creating a pre-release::

      VERSION=<version>

   For example, ``VERSION=3.0.1`` or ``VERSION=3.1a2``.

Release notes
-------------

1. Set GitHub user information into shell variables to ease copy-pasting the
   following command::

      GITHUB_USERNAME=<username>
      GITHUB_PASSWORD=<password>

   Alternatively, supply the credentials when running that command.

2. Generate a template for the release notes::

      invoke release-notes -w -v $VERSION -u $GITHUB_USERNAME -p $GITHUB_PASSWORD

   The ``-v $VERSION`` option can be omitted if `version is already set
   <Set version_>`__. Omit the ``-w`` option if you just want to get release
   notes printed to the console, not written to a file.

   When generating release notes for a preview release like ``3.0.2rc1``,
   the list of issues is only going to contain issues with that label
   (e.g. ``rc1``) or with a label of an earlier preview release (e.g.
   ``alpha1``, ``beta2``).

2. Fill the missing details in the generated release notes template.

3. Make sure that issues have correct information:

   - All issues should have type (bug, enhancement or task) and priority set.
     Notice that issues with the task type are automatically excluded from
     the release notes.
   - Issue priorities should be consistent.
   - Issue titles should be informative. Consistency is good here too, but
     no need to overdo it.

   If information needs to be added or edited, its better to edit it in the
   issue tracker than in the generated release notes. This allows re-generating
   the list of issues later if more issues are added.

4. Add, commit and push::

      git add docs/releasenotes/robotstatuschecker-$VERSION.rst
      git commit -m "Release notes for $VERSION" docs/releasenotes/robotstatuschecker-$VERSION.rst
      git push

5. Update later if necessary. Writing release notes is typically the biggest
   task when generating releases, and getting everything done in one go is
   often impossible.


Set version
-----------

1. Set version information in `<robotstatuschecker.py>`_::

      invoke set-version $VERSION

2. Commit and push changes::

      git commit -m "Updated version to $VERSION" robotstatuschecker.py
      git push



Tagging
-------

1. Create an annotated tag and push it::

      git tag -a v$VERSION -m "Release $VERSION"
      git push --tags

2. Add short release notes to GitHub's `releases page
   <https://github.com/robotframework/statuschecker/releases>`_
   with a link to the full release notes.

Creating distributions
----------------------

1. Checkout the earlier created tag if necessary::

      git checkout v$VERSION

   This isn't necessary if continuing right after tagging_.

2. Cleanup (again). This removes temporary files as well as ``build`` and
   ``dist`` directories::

      invoke clean

3. Create source distribution and universal (i.e. Python 2 and 3 compatible)
   `wheel <http://pythonwheels.com>`_::

      python -m build
      ls -l dist

   Distributions can be tested locally if needed.

4. Upload distributions to PyPI::

      twine upload dist/*

5. Verify that project the page at `PyPI
   <https://pypi.org/project/robotstatuschecker/>`_
   looks good.

6. Test installation (add ``--pre`` with pre-releases)::

      pip install --upgrade robotstatuschecker

Post actions
------------

1. Back to master if needed::

      git checkout master

2. Set dev version based on the previous version::

      invoke set-version dev
      git commit -m "Back to dev version" robotstatuschecker.py
      git push

   For example, ``1.2.3`` is changed to ``1.2.4.dev1`` and ``2.0.1a1``
   to ``2.0.1a2.dev1``.

3. Close the `issue tracker milestone
   <https://github.com/robotframework/statuschecker/milestones>`_.
   Create also new milestone for the next release unless one exists already.

4. Advertise on mailing lists, `Twitter <https://twitter.com/robotframework>`_,
   `LinkedIn <https://www.linkedin.com/groups/3710899>`_, and elsewhere as
   needed.
