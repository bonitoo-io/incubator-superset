# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
#from flask_appbuilder.security.manager import AUTH_OAUTH
import json


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...' \
                .format(var_name)
            raise EnvironmentError(error_msg)


POSTGRES_USER = get_env_variable('POSTGRES_USER')
POSTGRES_PASSWORD = get_env_variable('POSTGRES_PASSWORD')
POSTGRES_HOST = get_env_variable('POSTGRES_HOST')
POSTGRES_PORT = get_env_variable('POSTGRES_PORT')
POSTGRES_DB = get_env_variable('POSTGRES_DB')

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (POSTGRES_USER,
                                                           POSTGRES_PASSWORD,
                                                           POSTGRES_HOST,
                                                           POSTGRES_PORT,
                                                           POSTGRES_DB)

REDIS_HOST = get_env_variable('REDIS_HOST')
REDIS_PORT = get_env_variable('REDIS_PORT')


class CeleryConfig(object):
    BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERY_TASK_PROTOCOL = 1


CELERY_CONFIG = CeleryConfig
ENABLE_PROXY_FIX = True
LOG_LEVEL = "DEBUG"
MAPBOX_API_KEY = get_env_variable('MAPBOX_API_KEY')
ENABLE_JAVASCRIPT_CONTROLS = True
PROXY_FIX_CONFIG = {
    "x_for": 1,
    "x_proto": 1,
    "x_host": 1,
    "x_port": 1,
    "x_prefix": 1,
}

#Google oauth2 configuration.

#CSRF_ENABLED = True
#AUTH_TYPE = AUTH_OAUTH
#AUTH_USER_REGISTRATION = False
#AUTH_USER_REGISTRATION_ROLE = 'Public'
#auth_credentials = json.load(open(get_env_variable('GOOGLE_OAUTH_CREDENTIALS')))['web']
#OAUTH_PROVIDERS = [{
#    'name': 'google',
#    'whitelist': ['@webshopfly.com'],
#    'icon': 'fa-google',
#    'token_key': 'access_token',
#    'remote_app': {
#        'base_url': 'https://oauth2.googleapis.com/',
#        'request_token_params': {
#           'scope': 'email profile'
#        },
#        'request_token_url': None,
#        'access_token_url': auth_credentials['token_uri'],
#        'authorize_url': auth_credentials['auth_uri'],
#        'consumer_key': auth_credentials['client_id'],
#        'consumer_secret': auth_credentials['client_secret']
#    }
#}]

# Gitlab oauth2 configuration.
# OAUTH_PROVIDERS = [{
#        'name': 'gitlab',
#        'icon': 'fa-gitlab',
#        'token_key': get_env_variable('GITLAB_TOKEN_KEY'),
#        'remote_app': {
#                'base_url': 'https://gitlab.com/api/v4/user',
#                'request_token_params': {
#                        'scope': 'openid read_user'
#                },
#                'access_token_url': 'https://gitlab.com/oauth/token',
#                'authorize_url': 'https://gitlab.com/oauth/authorize',
#                'request_token_method': 'GET',
#                'access_token_method': 'POST',
#                'consumer_key': get_env_variable('GITLAB_CONSUMER_KEY'),
#                'consumer_secret': get_env_variable('GITLAB_CONSUMER_SECRET')
#        }
# }]
#
# from custom_sso_security_manager import CustomSsoSecurityManager
# CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
