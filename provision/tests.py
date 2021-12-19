from invoke import task

from . import common, start


@task
def run(context, path=""):
    """Run django tests with ``extra`` args for ``p`` tests.

    `p` means `params` - extra args for tests

    manage.py test <extra>
    """
    common.success(f"Tests {path} running ")
    return start.run_python(context, f"-m pytest {path}")
