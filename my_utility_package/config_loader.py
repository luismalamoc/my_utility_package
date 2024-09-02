import json
import os
import sys

import botocore
from aws_secretsmanager_caching import SecretCacheConfig, SecretCache
from botocore.exceptions import ClientError
from dotenv import load_dotenv

AWS_DEFAULT_REGION = 'AWS_DEFAULT_REGION'
SHARED_SECRET_NAMES_LIST = 'SHARED_SECRET_NAMES_LIST'
SERVICE_NAME = 'secretsmanager'


class ConfigLoader:
    """
    A class to load and manage application configurations from environment variables and AWS Secrets Manager.

    The ConfigLoader class initializes configurations from a .env file and, optionally, from AWS Secrets Manager.
    It provides methods to load and update configurations, including sensitive data stored in AWS Secrets Manager.

    Attributes:
    -----------
    configurations : dict
        A dictionary holding the loaded configuration settings.
    config_file : str
        The path to the .env configuration file.

    Methods:
    --------
    _get_app_configuration():
        Loads configurations from the environment and AWS Secrets Manager.

    _load_shared_secrets():
        Retrieves shared secrets from AWS Secrets Manager.

    _handle_secrets_from_aws(secret_name, region_name):
        Handles the retrieval and processing of secrets from AWS Secrets Manager.

    _load_configuration_from_env():
        Loads configurations from environment variables defined in the .env file.

    _retrieve_from_aws(secret_name, region_name):
        Retrieves a secret string from AWS Secrets Manager.
    """
    def __init__(self, config_file):
        self.configurations = dict()
        self.config_file = config_file
        self._get_app_configuration()

    def _get_app_configuration(self):
        try:
            configuration = self._load_configuration_from_env()
            if configuration is not None:
                self.configurations.update(configuration)
            shared_secrets = self._load_shared_secrets()
            if shared_secrets is not None:
                self.configurations.update(shared_secrets)
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('_get_app_configuration: {0} {1} {2}'.format(exc_type, fname, exc_tb.tb_lineno))
            print(error)
            raise error

    def _load_shared_secrets(self):
        shared_secrets = dict()
        env_list = self.configurations.get(SHARED_SECRET_NAMES_LIST)
        region_name = self.configurations.get(AWS_DEFAULT_REGION)
        if env_list is not None:
            secret_name_list = json.loads(self.configurations.get(SHARED_SECRET_NAMES_LIST))
            for secret_name in secret_name_list:
                shared_secrets.update(self._handle_secrets_from_aws(secret_name, region_name))
        return shared_secrets

    def _handle_secrets_from_aws(self, secret_name, region_name):
        if secret_name is None or region_name is None:
            return None
        if len(secret_name) > 0 and len(region_name) > 0:
            secrets = dict()
            aws_data = self._retrieve_from_aws(secret_name, region_name)
            if aws_data is None:
                return None
            if len(aws_data) > 0:
                secrets = json.loads(aws_data)
                for item_name, item_value in secrets.items():
                    secrets[item_name] = item_value
            return secrets

    def _load_configuration_from_env(self):
        configurations = dict()
        load_dotenv(self.config_file)
        for item_name, item_value in os.environ.items():
            configurations[item_name] = item_value
        return configurations

    def _retrieve_from_aws(self, secret_name, region_name):
        try:
            client = botocore.session.get_session().create_client(service_name=SERVICE_NAME, region_name=region_name)
            cache_config = SecretCacheConfig()
            cache = SecretCache(config=cache_config, client=client)
            return cache.get_secret_string(secret_name)
        except ClientError as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('_retrieve_configured_aws_secrets Error: {0} {1} {2}'.format(exc_type, fname, exc_tb.tb_lineno))
            raise error
