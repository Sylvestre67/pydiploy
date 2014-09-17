# -*- coding: utf-8 -*-

import os
from time import time

import fabric
import fabtools
import pydiploy
from fabric.api import env


def set_current():
    """
    Uses current directory for new release
    """
    fabric.api.sudo("ln -nfs %(current_release)s %(current_path)s"
                    % {'current_release': env.remote_current_release,
                       'current_path': env.remote_current_path})


def setup():
    """
    Configs stuff for deployement
    """
    fabric.api.sudo("mkdir -p %(remote_domain_path)s/{releases,shared}" %
                    {'remote_domain_path': env.remote_project_dir})
    fabric.api.sudo("mkdir -p %(remote_shared_path)s/{config,log}" %
                    {'remote_shared_path': env.remote_shared_path})
    fabric.api.execute(pydiploy.require.system.permissions)


def cleanup():
    """
    Cleans old stuff on remote server
    """
    if 'releases' in env and len(env.releases) >= env.keep_releases:
        directories = env.releases
        directories.reverse()
        del directories[:env.keep_releases]
        env.directories = ' '.join(["%(releases_path)s/%(release)s" %
                                   {'releases_path': env.remote_releases_path,
                                    'release': release} for release in directories])

        fabric.api.sudo("rm -rf %(directories)s" %
                        {'directories': env.directories})


def deploy_code():
    """
    Deploys code according to tag in env var
    """
    fabric.api.require('tag', provided_by=['tag', 'head'])
    fabric.api.require('remote_project_dir', provided_by=env.goals)
    tarball = pydiploy.require.git.archive(env.application_name,
                                           prefix='%s-%s/' % (env.application_name,
                                                              env.tag.lower()),
                                           tag=env.tag,
                                           remote=env.remote_repo_url)
    with fabric.api.lcd('/tmp'):
        fabric.api.local('tar xvf %s' % os.path.basename(tarball))

    # TODO: see if some excluded files / dir
    # are not in fact usefull in certain projects
    exclude_files = ['fabfile', 'MANIFEST.in', '*.ignore', 'docs',
                     'log', 'bin', 'manage.py',
                     '%s/wsgi.py' % env.root_package_name, '*.db',
                     '.gitignore']
    exclude_files += ['%s/settings/%s.py' % (env.root_package_name, goal)
                      for goal in env.goals]

    if env.has_key('excluded_files'):
        exclude_files += env.excluded_files
    if env.has_key('cfg_shared_files'):
        for cfg_shared_file in env.cfg_shared_files:
            cfg_present = fabtools.files.is_file(
                path='%s/config/%s' % (
                    env.remote_shared_path, os.path.basename(cfg_shared_file)),
                use_sudo=True)
            if cfg_present is None:
                fabtools.files.upload_template('/tmp/%s-%s/%s' % (
                                               env.application_name,
                                               env.tag.lower(),
                                               cfg_shared_file
                                               ),
                                               os.path.join(
                                               env.remote_shared_path, 'config'),
                                               use_sudo=True)

            exclude_files += cfg_shared_file

    env.remote_current_release = "%(releases_path)s/%(time).0f" % {
        'releases_path': env.remote_releases_path, 'time': time()}

    fabric.contrib.project.rsync_project(env.remote_current_release,
                                         '/tmp/%s-%s/' % (
                                             env.application_name, env.tag.lower(
                                             )),
                                         delete=True,
                                         extra_opts='--rsync-path="sudo -u %s rsync"' % env.remote_owner,
                                         exclude=exclude_files)

    fabric.api.sudo(
        'chown -R %(user)s:%(group)s %(project_dir)s' % {'user': env.remote_owner,
                                                         'group': env.remote_group,
                                                         'project_dir': env.remote_current_release})
    # symlink with new release
    fabric.api.execute(symlink)
    # set current directory with new release
    fabric.api.execute(set_current)

    # uploading manage.py template
    fabtools.files.upload_template('manage.py',
                                   os.path.join(
                                       env.remote_current_release, 'manage.py'),
                                   template_dir=env.local_tmp_root_app,
                                   context=env,
                                   use_sudo=True,
                                   user=env.remote_owner,
                                   chown=True,
                                   mode='744',
                                   use_jinja=True)

    # uploading wsgi.py template
    fabtools.files.upload_template('wsgi.py',
                                   os.path.join(
                                       env.remote_base_package_dir, 'wsgi.py'),
                                   template_dir=env.local_tmp_root_app_package,
                                   context=env,
                                   use_sudo=True,
                                   user=env.remote_owner,
                                   chown=True,
                                   mode='644',
                                   use_jinja=True)
    fabric.api.lcd('rm %s' % tarball)


def rollback_code():
    """
    Rolls back to the previously deployed version
    """
    if len(env.releases) >= 2:
        fabric.api.sudo("rm %(current_path)s; ln -s %(previous_release)s %(current_path)s && rm -rf %(current_release)s" %
                        {'current_release': env.current_release, 'previous_release': env.previous_release, 'current_path': env.remote_current_path})


def symlink():
    """
    Updates symlink stuff to the current deployed version
    """
    fabric.api.sudo("ln -nfs %(shared_path)s/log %(current_release)s/log" %
                    {'shared_path': env.remote_shared_path,
                     'current_release': env.remote_current_release})
    if env.has_key('cfg_shared_files'):
        for cfg_shared_file in env.cfg_shared_files:
            fabric.api.sudo("ln -nfs %(shared_path)s/config/%(file_name)s %(current_release)s/%(file)s" %
                            {'shared_path': env.remote_shared_path,
                             'current_release': env.remote_current_release,
                             'file': cfg_shared_file,
                             'file_name':  os.path.basename(cfg_shared_file)})
