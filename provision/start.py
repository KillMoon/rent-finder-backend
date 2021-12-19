from . import docker, is_local_python

##############################################################################
# Run commands
##############################################################################

__all__ = (
    "run_web",
    "run_web_python",
    "run_local_python",
)

WAIT_FOR_IT_FILE = "provision/wait-for-it.sh"
WAIT_FOR_IT_SCRIPT = f"./{WAIT_FOR_IT_FILE} postgres:5432 -- "


def run_web(context, command, watchers=()):
    """Run command in``web`` container.

    docker-compose run --rm web <command>
    """
    return docker.docker_compose_run(
        context,
        params="--rm --service-ports",
        container="web",
        command=command,
        watchers=watchers,
    )


def run_web_python(context, command, watchers=()):
    """Run command using web python interpreter."""
    return run_web(context, " ".join(["python3", command]), watchers=watchers)


def run_local_python(context, command: str, watchers=()):
    """Run command using local python interpreter."""
    docker.up(context)
    return context.run(
        " ".join([WAIT_FOR_IT_SCRIPT, "python3", command]),
        watchers=watchers,
    )


if is_local_python:
    run_python = run_local_python
else:
    run_python = run_web_python
