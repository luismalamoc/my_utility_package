import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from my_utility_package.database_connection import DatabaseConnection


@pytest.fixture
def mock_app_config():
    return {
        "DRIVER": "postgresql",
        "USER": "test_user",
        "PASSWORD": "test_password",
        "HOST": "localhost",
        "PORT": "5432",
        "DATABASE": "test_db",
        "TIMEOUT": "10"
    }


@patch('my_utility_package.database_connection.create_engine')
@patch('my_utility_package.database_connection.automap_base')
def test_connect_success(mock_automap_base, mock_create_engine, mock_app_config):
    mock_engine = MagicMock(spec=Engine)
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = True

    mock_base = MagicMock()
    mock_automap_base.return_value = mock_base

    db_conn = DatabaseConnection(app_config=mock_app_config)

    assert db_conn.get_engine() == mock_engine
    assert db_conn.session_factory is not None
    assert db_conn.get_metadata() == mock_base


@patch('my_utility_package.database_connection.create_engine')
def test_connect_failure(mock_create_engine, mock_app_config):
    mock_engine = MagicMock(spec=Engine)
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = False

    with pytest.raises(ConnectionError, match="Failed to connect to the Database"):
        DatabaseConnection(app_config=mock_app_config)


@patch('my_utility_package.database_connection.create_engine')
@patch('my_utility_package.database_connection.automap_base')
def test_get_metadata(mock_automap_base, mock_create_engine, mock_app_config):
    mock_engine = MagicMock(spec=Engine)
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = True

    mock_base = MagicMock()
    mock_automap_base.return_value = mock_base

    db_conn = DatabaseConnection(app_config=mock_app_config)
    metadata = db_conn.get_metadata()

    assert metadata == mock_base
