# -*- coding: utf-8 -*-

"""
"""

import os

from fabric.api import env
from fabric.api import cd
from fabric.api import run
from fabric.contrib.files import exists

import fabtools
from fabtools import require

from pydiploy.system import get_distant_home


def install(tmp_directory):
    """
    """
    with fabtools.python.virtualenv(env.virtualenv_dir):
        with cd(tmp_directory):
            run('python setup.py install')
            if exists('requirements/%s.txt' % env.env):
                require.python.requirements('requirements/%s.txt' % env.env)


def appdir(user, group, app_name):
    """
    """
    if not env.appdir:
        env.appdir = os.path.join(remote_home(user), app_name)
        require.directory(env.appdir, use_sudo=True, owner=user, group=group,
            mode='755')
    return env.appdir


def logdir(user, group, app_name):
    """
    """
    if not env.logdir:
        env.logdir = os.path.join(appdir(user, group, app_name), 'log')
        require.directory(env.logdir, use_sudo=True, owner=user, group=group,
                mode='755')
    return env.logdir