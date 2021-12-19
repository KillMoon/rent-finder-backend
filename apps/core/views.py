import platform
from collections import namedtuple

import django
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from libs.utils import get_changelog_html, get_latest_version

Changelog = namedtuple("Changelog", ["name", "text", "version", "open_api_ui"])

AGRO_CD_URL_MAPPING = dict(
    development="https://deploy.saritasa.rocks/",
    prod="TODO",
)
AGRO_CD_MAPPING = dict(
    development="rent-checker-dev",
    prod="rent-checker-prod",
)


class AppStatsMixin:
    """Add information about app to context."""

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        context.update(
            env=settings.ENVIRONMENT,
            version=get_latest_version("CHANGELOG.md"),
            python_version=platform.python_version(),
            django_version=django.get_version(),
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
            agro_cd_url=AGRO_CD_URL_MAPPING.get(
                settings.ENVIRONMENT, AGRO_CD_URL_MAPPING["development"],
            ),
            agro_cd_app=AGRO_CD_MAPPING.get(
                settings.ENVIRONMENT, AGRO_CD_MAPPING["development"],
            ),
        )
        return context


class IndexView(AppStatsMixin, TemplateView):
    """Class-based view for that shows version of open_api file on main page.

    Displays the current version of the open_api specification and changelog.

    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        context["changelog"] = Changelog(
            name=settings.SPECTACULAR_SETTINGS.get("TITLE"),
            text=get_changelog_html("CHANGELOG.md"),
            version=settings.SPECTACULAR_SETTINGS.get("VERSION"),
            open_api_ui=reverse_lazy("open_api:ui"),
        )
        return context
