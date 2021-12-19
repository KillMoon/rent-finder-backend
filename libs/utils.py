import os
import re

from mistune import markdown


def get_changelog_html(changelog_name: str) -> str:
    """Convert changelog text to html."""
    changelog_path = f"docs/{changelog_name}"
    if not os.path.exists(changelog_path):
        return ""

    with open(changelog_path) as file:
        changelog = file.read()

    return markdown(changelog)


def get_latest_version(changelog_filepath: str) -> str:
    """Get latest version from changelog file.

    Args:
        changelog_filepath (str):Path to changelog file

    Raises:
        ValueError: if we couldn"t find any versions in changelog file

    """
    version_regex = r"(?!### )\d{1,2}\.\d{1,2}\.\d{1,3}"
    re_rule = re.compile(version_regex)

    with open(f"docs/{changelog_filepath}") as file:
        for line in file:
            search = re_rule.search(line)
            if search:
                return search.group()

    raise ValueError(
        "Incorrect changelog file, couldn't find version number for "
        f"{changelog_filepath}",
    )
