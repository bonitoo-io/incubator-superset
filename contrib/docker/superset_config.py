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
 
def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...'\
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
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY', 'pk.eyJ1IjoibWlyZWttIiwiYSI6ImNqeDRseGE1bDAxazQ0MGxsejB4c2w4M2cifQ.RXrMiFyYHwjTwJop1-IZ5A')

#Gitlab oauth2 configuration.
#from flask_appbuilder.security.manager import AUTH_OAUTH

#AUTH_TYPE = AUTH_OAUTH
#AUTH_USER_REGISTRATION = True
#AUTH_USER_REGISTRATION_ROLE = 'Public'
#OAUTH_PROVIDERS = [{
#        'name': 'Gitlab',
#        'icon': 'fa-gitlab',
#        'token_key': 'KB4E3mfi5PNDzb4SRYBQ',
#        'remote_app': {
#                'base_url': 'https://gitlab.com/api/v4/user',
#                'request_token_params': {
#                        'scope': 'openid read_user'
#                },
#                'access_token_url': 'https://gitlab.com/oauth/token',
#                'authorize_url': 'https://gitlab.com/oauth/authorize',
#                'request_token_method': 'GET',
#                'access_token_method': 'POST',
#                'consumer_key': '10ee68db82e89bd792f7450d3495e6fc746cc909f23b7a5d6e71e7f6badddf39',
#                'consumer_secret': 'e9e33e2d406b7334a75d721f7068c76dc6b0fd1770464bdec7888eaf780c89a9'
#        }
#}]

#from custom_sso_security_manager import CustomSsoSecurityManager
#CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
