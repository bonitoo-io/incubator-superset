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

#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#

import logging
import os
import json

from cachelib.file import FileSystemCache
from flask_appbuilder.security.manager import (
    AUTH_OAUTH
)

logger = logging.getLogger()


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", 0)
REDIS_RESULTS_DB = get_env_variable("REDIS_CELERY_DB", 1)


RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

# Your App secret key
SECRET_KEY="\2\1thisismyscretkey\1\2\e\y\y\h"

class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab",)
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}
    CELERY_TASK_PROTOCOL = 1


CELERY_CONFIG = CeleryConfig
SQLLAB_CTAS_NO_LIMIT = True
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
APP_ICON = "/static/assets/images/superset-logo-flymeto.png"
APP_ICON_WIDTH = 126
FAVICONS = [{"href": "/static/assets/images/favicon-flymeto.png"}]

#Google oauth2 configuration.

CSRF_ENABLED = True
AUTH_TYPE = AUTH_OAUTH

# Uncomment to setup Full admin role name
#AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
#AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role for all users
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# Self registration role based on user info
#AUTH_USER_REGISTRATION_ROLE_JMESPATH = "contains(['alice@example.com', 'celine@example.com'], email) && 'Admin' || 'Public'"

auth_credentials = json.load(open(get_env_variable('GOOGLE_OAUTH_CREDENTIALS')))['web']
OAUTH_PROVIDERS = [{
   'name': 'google',
   'icon': 'fa-google',
   'token_key': 'access_token',
   'whitelist': ['@webshopfly.com','@bonitoo.io','@essensworld.com'],
   'remote_app': {
       'client_id': auth_credentials['client_id'],
       'client_secret': auth_credentials['client_secret'],
       'api_base_url': 'https://www.googleapis.com/oauth2/v2/',
       'client_kwargs': {
         'scope': 'email profile'
       },
       'request_token_url': None,
       'access_token_url': auth_credentials['token_uri'],
       'authorize_url': auth_credentials['auth_uri']
   }
}]

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
