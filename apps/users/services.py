from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from libs.notifications.email import DefaultEmailNotification

from . import models


def reset_user_password(
    user: models.User,
    email_subject: str,
    email_template: str,
) -> bool:
    """Reset user password.

    This will send to user an email with a link where user can enter new
    password.

    """
    return DefaultEmailNotification(
        subject=email_subject,
        recipient_list=[user.email],
        template=email_template,
        uid=urlsafe_base64_encode(force_bytes(user.pk)),
        token=PasswordResetTokenGenerator().make_token(user),
        app_url=settings.FRONTEND_URL,
        app_label=settings.APP_LABEL,
        new_password_url=settings.FRONTEND_URL + settings.NEW_PASSWORD_URL,
        user=user,
    ).send()
