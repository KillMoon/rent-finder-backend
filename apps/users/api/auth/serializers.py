from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

from ... import services
from ..serializers import UserSerializer

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.

    Copied form rest_framework.authtoken.serializers.AuthTokenSerializer

    """
    email = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict):
        """Escape warning."""

    def update(self, instance, validated_data):
        """Escape warning."""


class TokenSerializer(OpenApiSerializer):
    """Auth token for entire app."""
    expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.REST_KNOX['TOKEN_TTL']}",
    )
    token = serializers.CharField(help_text="Token itself")
    user = UserSerializer()


class PasswordResetSerializer(serializers.Serializer):
    """Request for resetting user's password."""
    EMAIL_SUBJECT = _("Password Reset")
    EMAIL_TEMPLATE = "users/emails/password_reset.html"
    email = serializers.EmailField(
        help_text="Email of account which password should be reset",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user: User = None

    def validate_email(self, email: str) -> str:
        """Check that we have user with input email."""
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(
                _("There is no user with such email"),
            )
        self._user = query.first()
        return email

    def create(self, validated_data: dict):
        return services.reset_user_password(
            email_subject=self.EMAIL_SUBJECT,
            email_template=self.EMAIL_TEMPLATE,
            user=self._user,
        )

    def update(self, instance, validated_data):
        """Escape warning."""


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Request for resetting user's password.

    Explanation of token and uid

    Example `MQ-5b2-e2c1ce64d63673f0e78f`, where `MQ` - is `uid` or user id and
    `5b2-e2c1ce64d63673f0e78f` - `token` for resetting password

    """

    password = serializers.CharField(
        max_length=128,
    )
    password_confirm = serializers.CharField(
        max_length=128,
    )
    uid = serializers.CharField()
    token = serializers.CharField()
    _token_generator = PasswordResetTokenGenerator()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user: User = None

    def validate_uid(self, uid: str) -> str:
        """Validate that uid can be decoded and it's valid."""
        try:
            user_pk = force_str(urlsafe_base64_decode(uid))
        except DjangoUnicodeDecodeError as error:
            raise ValidationError(_("Invalid uid")) from error
        query = User.objects.filter(pk=user_pk)
        if not query.exists():
            raise ValidationError(_("Invalid uid"))
        self._user = query.first()
        return uid

    def validate_token(self, token: str) -> str:
        """Validate token."""
        if not self._token_generator.check_token(self._user, token):
            raise ValidationError(_("Invalid token"))
        return token

    def validate(self, attrs):
        """Validate passwords."""
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError(
                    dict(password_confirm=_("Passwords mismatch")),
                )
        password_validation.validate_password(password, self._user)
        return attrs

    def create(self, validated_data: dict) -> User:
        password = self.validated_data["password"]
        self._user.set_password(password)
        self._user.save()
        return self._user

    def update(self, instance, validated_data):
        """Escape warning."""
