import pytest
from unittest.mock import Mock
from my_utility_package.check_api_key_decorator import INVALID_OR_MISSING_API_KEY, check_api_key


# Mock function to be decorated
def mock_function():
    return "Function executed"


def test_valid_api_key():
    # Create a mock request with a valid API key in the headers
    mock_request = Mock()
    mock_request.headers = {"X-API-Key": "valid_api_key"}

    # Define the expected APP_API_KEY
    decorator = check_api_key(REQUEST_FROM_ENDPOINT=mock_request, APP_API_KEY="valid_api_key")

    # Apply the decorator to the mock function
    decorated_function = decorator(mock_function)

    # Assert that the function executes successfully with a valid API key
    assert decorated_function() == "Function executed"


def test_missing_api_key():
    # Create a mock request with no API key in the headers
    mock_request = Mock()
    mock_request.headers = {}

    # Define the expected APP_API_KEY
    decorator = check_api_key(REQUEST_FROM_ENDPOINT=mock_request, APP_API_KEY="valid_api_key")

    # Apply the decorator to the mock function
    decorated_function = decorator(mock_function)

    # Assert that an AttributeError is raised due to the missing API key
    with pytest.raises(AttributeError) as exc_info:
        decorated_function()
    assert str(exc_info.value) == INVALID_OR_MISSING_API_KEY


def test_invalid_api_key():
    # Create a mock request with an invalid API key in the headers
    mock_request = Mock()
    mock_request.headers = {"X-API-Key": "invalid_api_key"}

    # Define the expected APP_API_KEY
    decorator = check_api_key(REQUEST_FROM_ENDPOINT=mock_request, APP_API_KEY="valid_api_key")

    # Apply the decorator to the mock function
    decorated_function = decorator(mock_function)
