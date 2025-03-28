from . import display
import platform

from .docker import Docker
from .rsyslog import Rsyslog
from .logrotate import LogRotate

def install(update, force):

    os_env = detect_os_env()
    dependency_classes = {"docker":Docker, "rsyslog":Rsyslog, "logrotate":LogRotate}
    dependency_instances = [
        dependency_cls(os_env, force) for dependency_cls in dependency_classes.values()
    ]

    if update:
        for dependency in dependency_instances:
            dependency.update()
    else:
        for dependency in dependency_instances:
            dependency.install()


def detect_os_env():
    os_env = {}
    os_env["system"] = platform.system()
    if os_env["system"] == "Linux":
        os_release = platform.freedesktop_os_release()
        os_env["os_id"] = os_release["ID"]
        os_env["codename"] = os_release.get(
            "UBUNTU_CODENAME", os_release.get("VERSION_CODENAME")
        )

    display.print_debug(os_env)
    return os_env
