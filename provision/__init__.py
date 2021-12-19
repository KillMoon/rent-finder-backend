import configparser

__all__ = ("PROJECT_INTERPRETER",)

INTERPRETER_WEB = "web"
INTERPRETER_LOCAL = "local"

# read config
# config should be saved in file with name ".invoke"
# Format:
# ## .invoke
# [Project]
# interpreter = local

config = configparser.ConfigParser({"interpreter": INTERPRETER_WEB})
config.read(".invoke")

PROJECT_INTERPRETER = INTERPRETER_LOCAL

if config.has_section("Project"):
    PROJECT_INTERPRETER = config.get("Project", "interpreter")

is_local_python = (PROJECT_INTERPRETER == INTERPRETER_LOCAL)
