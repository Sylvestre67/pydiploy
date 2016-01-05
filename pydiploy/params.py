# -*- coding: utf-8 -*-

""" This module sets required and optional params for the stuff to be deployed.


::

 default is python/django/circus/nginx deployement

 PARAMS = {
            'role': {
                     'required_params'  : {  key description },
                     'optional_params'  : {  key description }
                    }
          }
 ...

"""

PARAMS = {
    'default': {

        'required_params': {'user': "user for ssh",
                            'remote_owner': "remote server user",
                            'remote_group': "remote server user group",
                            'application_name': "name of wepapp",
                            'root_package_name': "name of app in webapp",
                            'remote_home': "remote home root",
                            'remote_python_version': "remote python version to use",
                            'remote_virtualenv_root': "remote virtualenv root",
                            'remote_virtualenv_dir': "remote virtualenv dir for wepapp",
                            'remote_repo_url': "git repository url",
                            'local_tmp_dir': "local tmp dir",
                            'remote_static_root': "root of static files",
                            'locale': "locale to use on remote",
                            'timezone': "timezone used on remote",
                            'keep_releases': "number of old releases to keep",
                            'roledefs': "Role to use to deploy",
                            'backends': "backend to use to deploy",
                            'server_name': "name of webserver",
                            'short_server_name': "short name of webserver",
                            'static_folder': "path of static folder",
                            'goal': "stage to use to deploy (dev,prod,test...)",
                            'socket_port': "port to use for socket"},

        'optional_params': {'excluded_files': "file(s) to exclude when deploying",
                            'extra_ppa_to_install': "extra ppa(s) to install on remote",
                            'extra_pkg_to_install': "extra package(s) to install on remote",
                            'cfg_shared_files': "shared file(s) to deploy in shared dir",
                            'extra_goals': "extra goal(s) to add to deploy",
                            'oracle_client_version': "oracle client version to install",
                            'oracle_download_url': "oracle client download url",
                            'oracle_remote_dir': "oracle remote directory",
                            'oracle_packages': "oracle packages to install",
                            'circus_package_name': "circus package name",
                            'dest_path': "destination path",
                            'nginx_location_extra_directives': "nginx location extra directive(s)",
                            'verbose_output': "verbose output (True/False)",
                            'no_config_test': "don't check config params (True/False)",
                            'req_pydiploy_version': "pydiploy version required for checking fabfile syntax",
                            'extra_symlink_dirs': 'extra dirs to symlink to shared folder',
                            'tag': 'tag to deploy',
                            'no_shared_sessions': 'if True add ip_hash to nginx config',
                            'server_ssl_on': 'use ssl on nginx',
                            'path_to_cert': 'ssl certificate path',
                            'path_to_cert_key': 'ssl cert key path',
                            'map_settings': 'settings to map in django settings files',
                            'maintenance_title': 'customize maintenance page title',
                            'maintenance_text': 'customize maintenance page text',
                            'nginx_force_start': 'if True, it forces to start nginx when nginx is not started',
                            'socket_host': 'force a socket host',
                            'no_circus_web': 'provides a way to not install circus-web',
                            'circus_backend': 'name of the backend to use with circus',
                            'chaussette_backend': 'name of the backend to use with chaussette',
                            'run_tests_command': 'name of the command to run tests',
                            'remote_repo_specific_folder': 'specify a subfolder for the remote repository',
                            'remote_media_folder': "remote folder of the application's media files",
                            'media_folder': "path of the application's media files"}

    },
    'simple': {

        'required_params': {'user': "user for ssh",
                            'remote_owner': "remote server user",
                            'remote_group': "remote server user group",
                            'application_name': "name of wepapp",
                            'root_package_name': "name of app in webapp",
                            'remote_home': "remote home root",
                            'remote_python_version': "remote python version to use",
                            'remote_virtualenv_root': "remote virtualenv root",
                            'remote_virtualenv_dir': "remote virtualenv dir for wepapp",
                            'remote_repo_url': "git repository url",
                            'local_tmp_dir': "local tmp dir",
                            # 'remote_static_root': "root of static files",
                            'locale': "locale to use on remote",
                            'timezone': "timezone used on remote",
                            'keep_releases': "number of old releases to keep",
                            'roledefs': "Role to use to deploy",
                            # 'backends': "backend to use to deploy",
                            # 'server_name': "name of webserver",
                            # 'short_server_name': "short name of webserver",
                            # 'static_folder': "path of static folder",
                            'goal': "stage to use to deploy (dev,prod,test...)"
                            # 'socket_port': "port to use for socket"
                            },

        'optional_params': {'excluded_files': "file(s) to exclude when deploying",
                            'extra_ppa_to_install': "extra ppa(s) to install on remote",
                            'extra_pkg_to_install': "extra package(s) to install on remote",
                            'cfg_shared_files': "shared file(s) to deploy in shared dir",
                            'extra_goals': "extra goal(s) to add to deploy",
                            # 'oracle_client_version': "oracle client version to install",
                            # 'oracle_download_url': "oracle client download url",
                            # 'oracle_remote_dir': "oracle remote directory",
                            # 'oracle_packages': "oracle packages to install",
                            # 'circus_package_name': "circus package name",
                            'dest_path': "destination path",
                            # 'nginx_location_extra_directives': "nginx location extra directive(s)",
                            'verbose_output': "verbose output (True/False)",
                            'no_config_test': "don't check config params (True/False)",
                            'req_pydiploy_version': "pydiploy version required for checking fabfile syntax",
                            'extra_symlink_dirs': 'extra dirs to symlink to shared folder',
                            'tag': 'tag to deploy',
                            # 'no_shared_sessions': 'if True add ip_hash to nginx config',
                            # 'server_ssl_on': 'use ssl on nginx',
                            # 'path_to_cert': 'ssl certificate path',
                            # 'path_to_cert_key': 'ssl cert key path',
                            'map_settings': 'settings to map in django settings files',
                            # 'maintenance_title': 'customize maintenance page title',
                            # 'maintenance_text': 'customize maintenance page text',
                            # 'nginx_force_start': 'if True, it forces to start nginx when nginx is not started',
                            # 'socket_host': 'force a socket host',
                            # 'no_circus_web': 'provides a way to not install circus-web',
                            # 'circus_backend': 'name of the backend to use with circus',
                            # 'chaussette_backend': 'name of the backend to use with chaussette',
                            'run_tests_command': 'name of the command to run tests',
                            'remote_repo_specific_folder': 'specify a subfolder for the remote repository',
                            # 'remote_media_folder': "remote folder of the application's media files"
                            # 'media_folder': "path of the application's media files"
                            'server_name': "if you want to use an url for the name of the remote app folder instead of the application name (manual bottle or flask app)",
                            }

    }
}
