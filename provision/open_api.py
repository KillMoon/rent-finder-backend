from invoke import task

from . import common, django, system


@task
def validate_swagger(context):
    """Check that generated open_api spec is valid.

    It creates spec file in ./tmp folder and then validates it.

    """
    common.success("Validating OpenApi spec")
    system.create_tmp_folder(context)
    django.manage(
        context,
        "spectacular --file .tmp/schema.yaml --validate --fail-on-warn",
    )
