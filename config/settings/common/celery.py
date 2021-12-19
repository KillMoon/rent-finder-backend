CELERY_TASK_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["pickle", "json"]

# if this option is True - celery task will run like default functions,
# not asynchronous
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = False
# Raise error for eager task
CELERY_TASK_EAGER_PROPAGATES = True

# specify connection options for task producer, so it won’t retry forever if
# the broker isn’t available at the first task execution
CELERY_BROKER_TRANSPORT_OPTIONS = {'max_retries': 3, 'socket_timeout': 5}
