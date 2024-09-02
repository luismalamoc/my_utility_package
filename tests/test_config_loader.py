import pytest
from unittest.mock import patch, MagicMock
import os
import json
from my_utility_package.config_loader import ConfigLoader, SHARED_SECRET_NAMES_LIST, \
    AWS_DEFAULT_REGION  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_env_file(tmpdir):
    env_file = tmpdir.join('.env')
    env_file.write('KEY1=value1\nKEY2=value2')
    return str(env_file)


@pytest.fixture
def mock_aws_secrets():
    return json.dumps({
        "SECRET_KEY1": "secret_value1",
        "SECRET_KEY2": "secret_value2"
    })


def test_load_configuration_from_env(mock_env_file):
    loader = ConfigLoader(config_file=mock_env_file)
    assert loader.configurations['KEY1'] == 'value1'
    assert loader.configurations['KEY2'] == 'value2'


@patch('my_utility_package.config_loader.ConfigLoader._retrieve_from_aws')
def test_load_shared_secrets(mock_retrieve_from_aws, mock_env_file, mock_aws_secrets):
    mock_retrieve_from_aws.return_value = mock_aws_secrets

    os.environ[SHARED_SECRET_NAMES_LIST] = json.dumps(["dummy_secret"])
    os.environ[AWS_DEFAULT_REGION] = "us-west-2"

    loader = ConfigLoader(config_file=mock_env_file)

    assert loader.configurations['SECRET_KEY1'] == 'secret_value1'
    assert loader.configurations['SECRET_KEY2'] == 'secret_value2'


@patch('my_utility_package.config_loader.ConfigLoader._retrieve_from_aws')
def test_handle_secrets_from_aws(mock_retrieve_from_aws, mock_aws_secrets):
    mock_retrieve_from_aws.return_value = mock_aws_secrets

    loader = ConfigLoader(config_file=None)

    secrets = loader._handle_secrets_from_aws("dummy_secret", "us-west-2")

    assert secrets['SECRET_KEY1'] == 'secret_value1'
    assert secrets['SECRET_KEY2'] == 'secret_value2'


def test_get_app_configuration_exception(mock_env_file):
    with patch('my_utility_package.config_loader.ConfigLoader._load_configuration_from_env',
               side_effect=Exception("Error loading env")):
        with pytest.raises(Exception, match="Error loading env"):
            ConfigLoader(config_file=mock_env_file)
