from pathlib import Path

from invoke import task
from rellu import initialize_labels, ReleaseNotesGenerator, Version
from rellu.tasks import clean  # noqa

VERSION_PATTERN = '__version__ = "(.*)"'
REPOSITORY = "robotframework/statuschecker"
VERSION_PATH = Path("robotstatuschecker.py")
RELEASE_NOTES_PATH = Path("docs/releasenotes/robotstatuschecker-{version}.rst")
RELEASE_NOTES_TITLE = "robotstatuschecker {version}"
RELEASE_NOTES_INTRO = """
StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 1.4 and newer are compatible both with Python 2 and Python 3.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3A{version.milestone}
"""

@task
def set_version(ctx, version):
    """Set project version in `robotstatuschecker.py`` file.
    Args:
        version: Project version to set or ``dev`` to set development version.
    Following PEP-440 compatible version numbers are supported:
    - Final version like 3.0 or 3.1.2.
    - Alpha, beta or release candidate with ``a``, ``b`` or ``rc`` postfix,
      respectively, and an incremented number like 3.0a1 or 3.0.1rc1.
    - Development version with ``.dev`` postfix and an incremented number like
      3.0.dev1 or 3.1a1.dev2.
    When the given version is ``dev``, the existing version number is updated
    to the next suitable development version. For example, 3.0 -> 3.0.1.dev1,
    3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    version.write()
    print(version)


@task
def print_version(ctx):
    """Print the current project version."""
    print(Version(path=VERSION_PATH, pattern=VERSION_PATTERN))
