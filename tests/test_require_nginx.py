#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from unittest import TestCase

from fabric.api import env
from mock import call, Mock, patch
from pydiploy.require.nginx import (down_site_config, nginx_pkg, nginx_reload,
                                    nginx_restart, root_web, up_site_config,
                                    web_configuration, web_static_files)


class NginxCheck(TestCase):

    """
    nginx test
    """

    def setUp(self):
        self.previous_env = copy.deepcopy(env)
        env.remote_static_root = "remote_static_root"
        env.local_tmp_dir = 'local_tmp_dir'
        env.server_name = "server_name"
        env.lib_path = "lib_path"
        env.application_name = "application_name"

    def tearDown(self):
        env.clear()
        env.update(self.previous_env)

    @patch('fabtools.require.files.directory', return_value=Mock())
    def test_root_web(self, files_directory):
        root_web()
        self.assertTrue(files_directory.called)
        self.assertEqual(files_directory.call_args, call(
            'remote_static_root', owner='root', use_sudo=True, group='root', mode='755'))

    @patch('fabtools.require.deb.packages', return_value=Mock())
    def test_nginx_pkg(self, deb_packages):
        nginx_pkg()
        self.assertTrue(deb_packages.called)
        self.assertEqual(deb_packages.call_args, call(['nginx'], update=False))

    @patch('fabtools.service.is_running', return_value=True)
    @patch('fabtools.service.start', return_value=Mock())
    @patch('fabtools.service.reload', return_value=Mock())
    def test_nginx_reload(self, reload, start, is_running):
        nginx_reload()
        self.assertTrue(reload.called)
        self.assertEqual(reload.call_args, call('nginx'))
        self.assertTrue(is_running.called)
        self.assertFalse(start.called)

        is_running.return_value = False
        reload.called = False
        is_running.called = False
        start.called = False

        nginx_reload()

        self.assertTrue(is_running.called)
        self.assertFalse(reload.called)
        self.assertTrue(start.called)
        self.assertEqual(start.call_args, call('nginx'))

    @patch('fabtools.service.is_running', return_value=True)
    @patch('fabtools.service.start', return_value=Mock())
    @patch('fabtools.service.restart', return_value=Mock())
    def test_nginx_restart(self, restart, start, is_running):
        nginx_restart()
        self.assertTrue(is_running.called)
        self.assertFalse(start.called)
        self.assertTrue(restart.called)

        is_running.return_value = False
        restart.called = False
        is_running.called = False
        start.called = False

        nginx_restart()

        self.assertFalse(restart.called)
        self.assertTrue(is_running.called)
        self.assertTrue(start.called)
        self.assertEqual(start.call_args, call('nginx'))

    @patch('fabric.contrib.project.rsync_project', return_value=Mock())
    def test_web_static_files(self, rsync_project):
        web_static_files()
        self.assertTrue(rsync_project.called)
        self.assertEqual(rsync_project.call_args,
                         call('remote_static_root/application_name', 'local_tmp_dir/assets/', extra_opts='--rsync-path="sudo rsync"', delete=True, ssh_opts='-t'))

    @patch('fabtools.files.upload_template', return_value=Mock())
    @patch('fabtools.files.is_link', return_value=True)
    @patch('fabric.api.cd', return_value=Mock())
    @patch('fabric.api.sudo', return_value=Mock())
    def test_web_configuration(self, api_sudo, api_cd, is_link, upload_template):
        api_cd.return_value.__exit__ = Mock()
        api_cd.return_value.__enter__ = Mock()

        web_configuration()

        is_link.return_value = False

        web_configuration()

        self.assertTrue(api_cd.called)
        self.assertEqual(api_cd.call_args,
                         call('/etc/nginx/sites-enabled'))

        self.assertTrue(api_sudo.called)
        self.assertEqual(api_sudo.call_args,
                         call('ln -s /etc/nginx/sites-available/server_name.conf .'))

    @patch('fabtools.files.upload_template', return_value=Mock())
    @patch('fabtools.files.is_link', return_value=True)
    @patch('fabric.api.cd', return_value=Mock())
    @patch('fabric.api.sudo', return_value=Mock())
    def test_up_site_conf(self, api_sudo, api_cd, is_link, upload_template):
        api_cd.return_value.__exit__ = Mock()
        api_cd.return_value.__enter__ = Mock()

        up_site_config()

        self.assertTrue(upload_template.called)
        self.assertTrue(
            str(upload_template.call_args).find("'nginx.conf.tpl'") > 0)
        self.assertTrue(str(upload_template.call_args).find(
            "'/etc/nginx/sites-available/server_name.conf'") > 0)
        self.assertTrue(str(upload_template.call_args)
                        .find("template_dir='lib_path/templates'") > 0)

        self.assertTrue(upload_template.is_link)

        is_link.return_value = False

        up_site_config()

        self.assertTrue(api_cd.called)
        self.assertEqual(api_cd.call_args,
                         call('/etc/nginx/sites-enabled'))

        self.assertTrue(api_sudo.called)
        self.assertEqual(api_sudo.call_args, call(
            'ln -s /etc/nginx/sites-available/server_name.conf .'))

    @patch('fabtools.files.upload_template', return_value=Mock())
    @patch('fabtools.files.is_link', return_value=True)
    @patch('fabric.api.cd', return_value=Mock())
    @patch('fabric.api.sudo', return_value=Mock())
    def test_down_site_conf(self, api_sudo, api_cd, is_link, upload_template):
        api_cd.return_value.__exit__ = Mock()
        api_cd.return_value.__enter__ = Mock()

        down_site_config()

        self.assertTrue(upload_template.called)
        self.assertTrue(
            str(upload_template.call_args).find("'nginx_down.conf.tpl'") > 0)
        self.assertTrue(str(upload_template.call_args).find(
            "'/etc/nginx/sites-available/server_name_down.conf'") > 0)
        self.assertTrue(str(upload_template.call_args)
                        .find("template_dir='lib_path/templates'") > 0)

        self.assertTrue(upload_template.is_link)

        is_link.return_value = False

        down_site_config()

        # self.assertTrue(api_cd.called)
        # self.assertEqual(api_cd.call_args,
        #                  call('/etc/nginx/sites-enabled'))

        # self.assertTrue(api_sudo.called)
        # self.assertEqual(api_sudo.call_args, call(
        #     'ln -s /etc/nginx/sites-available/server_name.conf .'))
