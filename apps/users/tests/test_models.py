from django.core.exceptions import ValidationError

import pytest

from ..factories import UserFactory
from ..models import User


@pytest.fixture(scope="module")
def user(django_db_setup, django_db_blocker):
    """Module-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = UserFactory()
        yield created_user
        created_user.delete()


def test_unique_email_validation(user):
    """Test validation for case insensitive unique email."""
    new_user = User(email=user.email.upper(), password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
    assert "email" in exc.value.error_dict
