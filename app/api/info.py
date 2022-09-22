import logging
import os
import platform
import subprocess
from datetime import datetime

import flask


def get_git_version():
    try:
        return (
            subprocess.check_output('git describe --always'.split())
            .decode()
            .strip()
        )
    except Exception:
        logging.warning("Could not get version info from git", exc_info=True)
        return None


def get_info():
    now = datetime.utcnow()
    os_release = platform.freedesktop_os_release() or {}
    name = os_release.get('PRETTY_NAME') or os.release.get('NAME') or os.name
    return {
        'version': get_git_version(),
        'time': now.timestamp(),
        'datetime': now,
        'software': {
            'flask': flask.__version__,
            'python': platform.python_version(),
            'system': {
                'name': name,
                'platform': platform.system(),
                'release': platform.release(),
                'arch': platform.machine(),
            },
        },
    }
