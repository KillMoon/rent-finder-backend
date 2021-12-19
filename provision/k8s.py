##############################################################################
# Shortcuts for k8s
##############################################################################
import os

from invoke import Responder, task

from . import common

NAMESPACE = "rent-checker"

POSTGRES_POD = (
    "kubectl get pods -n postgres "
    "--selector=app=saritasa-rocks-psql "
    "-o jsonpath='{.items[*].metadata.name}'"
)


def _get_pod_cmd(component: str) -> str:
    """Get command for getting exact pod."""
    return (
        f"kubectl get pods "
        f"-l app.kubernetes.io/component={component} "
        f"--no-headers -o=\"custom-columns=NAME:.metadata.name\""
    )


@task
def login(context):
    """Login into k8s via teleport."""
    common.success("Login into kubernetes CI")
    context.run("tsh login --proxy=teleport.saritasa.rocks:443 --auth=github")


@task
def set_context(context):
    """Set k8s context to current project."""
    common.success("Setting context for k8s")
    context.run(
        f"kubectl config set-context --current --namespace={NAMESPACE}",
    )


@task(pre=[set_context])
def logs(context, component="backend"):
    """Get logs for k8s pod."""
    common.success(f"Getting logs from {component}")
    context.run(f"kubectl logs $({_get_pod_cmd(component)})")


@task(pre=[set_context])
def pods(context):
    """Get pods from k8s."""
    common.success("Getting pods")
    context.run("kubectl get pods")


@task(pre=[set_context])
def execute(
    context,
    entry="/cnb/lifecycle/launcher bash",
    component="backend",
    pty=None,
    hide=None,
):
    """Execute command inside of k8s pod."""
    common.success(f"Entering into {component} with {entry}")
    return context.run(
        f"kubectl exec -ti $({_get_pod_cmd(component)}) -- {entry}",
        pty=pty,
        hide=hide,
    )


@task
def python_shell(context, component="backend"):
    """Enter into python shell."""
    execute(context, component=component, entry="shell_plus")


@task
def health_check(context, component="backend"):
    """Check health of component."""
    execute(context, component=component, entry="health_check")


@task
def get_remote_config(
    context,
    component="backend",
    path_to_config="/workspace/app/config/settings/config.py",
):
    """Get config from pod."""
    return execute(
        context,
        component=component,
        entry=f"cat {path_to_config}",
        pty=False,
        hide="out",
    ).stdout


@task
def postgres_create_dump(
    context,
    command,
    password,
):
    """Execute command in postgres pod."""
    common.success(f"Entering into postgres with {command}")
    context.run(
        f"kubectl exec -ti -n postgres $({POSTGRES_POD}) -- {command}",
        watchers=[
            Responder(
                pattern="Password: ",
                response=f"{password}\n",
            ),
        ],
    )


@task
def postgres_get_dump(
    context,
    file_name=f"{NAMESPACE}_db_dump.sql",
):
    """Download db data from postgres pod if it present."""
    common.success(f"Downloading dump({file_name}) from pod")
    current_folder = os.getcwd()
    context.run(
        f"kubectl cp -n postgres "
        f"$({POSTGRES_POD}):tmp/{file_name} {current_folder}/{file_name}",
    )
    common.success(f"Downloaded dump({file_name}) from pod. Clean up")
    rm_command = f"rm tmp/{file_name}"
    context.run(
        f"kubectl exec -ti -n postgres $({POSTGRES_POD}) -- {rm_command}",
    )
