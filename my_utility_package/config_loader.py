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
    A class to load and manage application configurations from environment variables, configuration files,
    and AWS Secrets Manager.

    The `ConfigLoader` class is responsible for loading configurations from a `.env` file, updating them with
    shared secrets retrieved from AWS Secrets Manager, and making these configurations available to the application.

    Attributes:
    -----------
    configurations : dict
        A dictionary holding the application's configuration parameters.
    config_file : str
        The path to the configuration file (typically a .env file) from which environment variables are loaded.

    Methods:
    --------
    __init__(self, config_file):
        Initializes the ConfigLoader with the given configuration file and loads the initial configurations.

    _get_app_configuration(self):
        Loads the application configuration by combining environment variables and shared secrets.

    _load_shared_secrets(self):
        Retrieves and loads shared secrets from AWS Secrets Manager into the configurations dictionary.

    _handle_secrets_from_aws(self, secret_name, region_name):
        Fetches secrets from AWS Secrets Manager for a given secret name and region.

    _load_configuration_from_env(self):
        Loads configurations from the environment variables set in the provided .env file.

    _retrieve_from_aws(self, secret_name, region_name):
        Retrieves the secret string from AWS Secrets Manager for a given secret name and region.
    """

    def __init__(self, config_file):
        """
        Initializes the ConfigLoader with the specified configuration file.

        Parameters:
        -----------
        config_file : str
            The path to the .env configuration file from which environment variables are loaded.

        Initializes the `configurations` dictionary and calls the `_get_app_configuration` method to load
        configurations from the environment and AWS Secrets Manager.
        """
        self.configurations = dict()
        self.config_file = config_file
        self._get_app_configuration()

    def _get_app_configuration(self):
        """
        Loads the application configuration by combining configurations from environment variables
        and shared secrets from AWS Secrets Manager.

        This method first loads configurations from the environment variables specified in the `.env` file.
        Then, it attempts to load any shared secrets from AWS Secrets Manager and merges them into the
        `configurations` dictionary.

        Raises:
        -------
        Exception
            If any error occurs during the loading of configurations, the error is logged and re-raised.
        """
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
        """
        Loads shared secrets from AWS Secrets Manager.

        This method retrieves a list of secret names from the environment variables, and for each secret name,
        it fetches the corresponding secrets from AWS Secrets Manager and merges them into the `configurations`
        dictionary.

        Returns:
        --------
        dict
            A dictionary containing the shared secrets retrieved from AWS Secrets Manager, or an empty dictionary
            if no secrets are found.
        """
        shared_secrets = dict()
        env_list = self.configurations.get(SHARED_SECRET_NAMES_LIST)
        region_name = self.configurations.get(AWS_DEFAULT_REGION)
        if env_list is not None:
            secret_name_list = json.loads(self.configurations.get(SHARED_SECRET_NAMES_LIST))
            for secret_name in secret_name_list:
                shared_secrets.update(self._handle_secrets_from_aws(secret_name, region_name))
        return shared_secrets

    def _handle_secrets_from_aws(self, secret_name, region_name):
        """
        Retrieves secrets from AWS Secrets Manager for a given secret name and region.

        Parameters:
        -----------
        secret_name : str
            The name of the secret to retrieve from AWS Secrets Manager.
        region_name : str
            The AWS region where the secret is stored.

        Returns:
        --------
        dict
            A dictionary containing the secrets fetched from AWS Secrets Manager, or None if no secrets are found.

        Notes:
        ------
        If either `secret_name` or `region_name` is None or empty, the method returns None.
        """
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
        """
        Loads configurations from environment variables defined in the .env file.

        This method loads environment variables from the .env file specified in the `config_file` and stores
        them in the `configurations` dictionary.

        Returns:
        --------
        dict
            A dictionary containing the environment variables loaded from the .env file.
        """
        configurations = dict()
        load_dotenv(self.config_file)
        for item_name, item_value in os.environ.items():
            configurations[item_name] = item_value
        return configurations

    def _retrieve_from_aws(self, secret_name, region_name):
        """
        Retrieves the secret string from AWS Secrets Manager for a given secret name and region.

        Parameters:
        -----------
        secret_name : str
            The name of the secret to retrieve from AWS Secrets Manager.
        region_name : str
            The AWS region where the secret is stored.

        Returns:
        --------
        str
            The secret string retrieved from AWS Secrets Manager.

        Raises:
        -------
        ClientError
            If an error occurs during the retrieval of the secret, the error is logged and re-raised.
        """
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
