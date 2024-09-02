import pytest
from unittest.mock import MagicMock
from my_utility_package.conditioned_dummy_response_decorator import conditioned_dummy_response


@pytest.fixture
def mock_route_func():
    return MagicMock(return_value=("Original Response", 200))


def test_dummy_mode_active(mock_route_func):
    dummy_response = {"message": "This is a dummy response"}
    decorator = conditioned_dummy_response(DUMMY_ACTIVE=True, DUMMY_RESPONSE=dummy_response)

    # Apply the decorator to the mock route function
    decorated_func = decorator(mock_route_func)

    # Call the decorated function
    response, status_code = decorated_func()

    # Assert that the dummy response is returned
    assert response == dummy_response
    assert status_code == 200
    mock_route_func.assert_not_called()


def test_dummy_mode_inactive(mock_route_func):
    decorator = conditioned_dummy_response(DUMMY_ACTIVE=False, DUMMY_RESPONSE={"message": "This is a dummy response"})

    # Apply the decorator to the mock route function
    decorated_func = decorator(mock_route_func)

    # Call the decorated function
    response, status_code = decorated_func()

    # Assert that the original route function is called and its response is returned
    assert response == "Original Response"
    assert status_code == 200
    mock_route_func.assert_called_once()


def test_dummy_mode_no_dummy_response(mock_route_func):
    # This test ensures that even if no dummy response is provided, the function behaves as expected.
    decorator = conditioned_dummy_response(DUMMY_ACTIVE=True, DUMMY_RESPONSE=None)

    # Apply the decorator to the mock route function
    decorated_func = decorator(mock_route_func)

    # Call the decorated function
    response, status_code = decorated_func()

    # Assert that None is returned as the response with a status code of 200
    assert response is None
    assert status_code == 200
    mock_route_func.assert_not_called()
