import fastapi
from fastapi import APIRouter
import subprocess
import platform
import os
import logging
from datetime import datetime


router = APIRouter()


def get_git_version():
    try:
        return subprocess.check_output('git describe --always'.split()).strip()
    except Exception:
        logging.warning("Could not get version info from git", exc_info=True)
        return None


@router.get('/')
def info():
    now = datetime.now()
    return {
        'version': get_git_version(),
        'time': now.timestamp(),
        'datetime': now,
        'software': {
            'fastapi': fastapi.__version__,
            'python': platform.python_version(),
            'system': {
                'name': os.name,
                'platform': platform.system(),
                'release': platform.release(),
                'arch': platform.machine(),
            },
        },
    }
