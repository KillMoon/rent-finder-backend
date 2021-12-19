# Settings for custom health checks
HEALTH_CHECKS_APPS = (
    "health_check",
    "health_check.db",
    "health_check.storage",
    "health_check.contrib.celery_ping",
    "health_check.contrib.redis",
    "libs.health_checks",
)
