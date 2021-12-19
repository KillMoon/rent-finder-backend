from rest_framework import exceptions
from rest_framework.views import exception_handler


def custom_exception_handler_simple(exc, context):
    """Handle simple drf exceptions.

    This custom exception handler for django REST framework wraps
    ValidationErrors into field `data` and adds `detail` field with
    first non field error or message:
        Unfortunately, there are some problems with the data you committed

    """
    if isinstance(exc, exceptions.ValidationError):
        if "non_field_errors" in exc.detail:
            exc.detail = {
                "data": exc.detail,
                "detail": exc.detail["non_field_errors"][0],
            }
        else:
            exc.detail = {
                "data": exc.detail,
                "detail": "Unfortunately, there are some problems with "
                "the data you committed",
            }

    return exception_handler(exc, context)
