"""Configuration file for pytest
"""
from django.conf import settings

import pytest


def pytest_configure():
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.
    """
    settings.DEBUG = False
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/3.0/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup):
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
# pylint: disable=invalid-name
def enable_db_access_for_all_tests(django_db_setup, db):
    """This hook allows all tests to access DB."""


@pytest.fixture(scope="session", autouse=True)
def temp_directory_for_media(tmpdir_factory):
    """Fixture that set temp directory for all media files.

    This fixture changes FILE_STORAGE to filesystem and provides temp dir for
    media. PyTest cleans up this temp dir by itself after few test runs
    """
    settings.DEFAULT_FILE_STORAGE = (
        "django.core.files.storage.FileSystemStorage"
    )
    media = tmpdir_factory.mktemp("tmp_media")
    settings.MEDIA_ROOT = media
