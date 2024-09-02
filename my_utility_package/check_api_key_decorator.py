X_API_KEY = "X-API-Key"
INVALID_OR_MISSING_API_KEY = "API key is invalid or is missing."


def check_api_key(**func_param):
    """
    Decorator to check the presence and validity of an API key in the request header.

    This decorator ensures that the API key provided in the request headers matches
    the expected API key. If the API key is valid, the decorated function is executed.
    Otherwise, an `AttributeError` is raised with a message indicating that the API key
    is invalid or missing.

    Parameters:
    -----------
    **func_param : dict
        A dictionary containing the following keys:
            - 'REQUEST_FROM_ENDPOINT' (request object): The request object from which the API key is extracted.
            - 'APP_API_KEY' (str): The expected API key that the request's API key should match.

    Returns:
    --------
    function
        The decorated function, if the API key is valid.

    Raises:
    -------
    AttributeError
        If the API key is missing or does not match the expected value, an `AttributeError` is raised
        with the message: "API key is invalid or is missing."

    Example:
    --------
    ```python
    from flask import request, jsonify

    APP_API_KEY = "your_expected_api_key"

    @check_api_key(REQUEST_FROM_ENDPOINT=request, APP_API_KEY=APP_API_KEY)
    def protected_endpoint():
        return jsonify({"message": "Access granted!"})
    ```
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            api_key_header_value = func_param["REQUEST_FROM_ENDPOINT"].headers.get(X_API_KEY)
            if (api_key_header_value is not None and func_param["APP_API_KEY"] is not None):
                if api_key_header_value == func_param["APP_API_KEY"]:
                    return func(*args, **kwargs)
                else:
                    raise AttributeError(INVALID_OR_MISSING_API_KEY)
            else:
                raise AttributeError(INVALID_OR_MISSING_API_KEY)

        return wrapper

    return decorator
