from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthChecksConfig(AppConfig):
    """Config for custom health check."""
    name = "libs.health_checks"

    def ready(self):
        """Register all custom checks in health check plugins"""
        from . import backends
        backends_to_register = (
            backends.EmailHealthCheck,
        )
        for backend in backends_to_register:
            plugin_dir.register(backend)
