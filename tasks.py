import sys
from pathlib import Path

from invoke import task
from rellu import ReleaseNotesGenerator, Version, initialize_labels
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
"""  # noqa


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


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):
    """Generates release notes based on issues in the issue tracker.
    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise just print them to the
                  terminal.
    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    folder = RELEASE_NOTES_PATH.parent.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(REPOSITORY, RELEASE_NOTES_TITLE, RELEASE_NOTES_INTRO)
    generator.generate(version, username, password, file)


@task
def init_labels(ctx, username=None, password=None):
    """Initialize project by setting labels in the issue tracker.
    Args:
        username: GitHub username.
        password: GitHub password.
    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively.
    Should only be executed once when taking ``rellu`` tooling to use or
    when labels it uses have changed.
    """
    initialize_labels(REPOSITORY, username, password)


@task
def lint(ctx):
    """Run linters

    Flake8, Black and robotframework-tidy
    """
    ctx.run("black --config pyproject.toml tasks.py robotstatuschecker.py")
    ctx.run("flake8 --config .flake8 tasks.py robotstatuschecker.py")
    ctx.run("isort tasks.py robotstatuschecker.py")
    tidy_command = [
        "robotidy",
        "--lineseparator",
        "unix",
        "--configure",
        "NormalizeAssignments:equal_sign_type=space_and_equal_sign",
        "--configure",
        "NormalizeAssignments:equal_sign_type_variables=space_and_equal_sign",
        "test",
    ]
    ctx.run(" ".join(tidy_command))
