X_API_KEY = "X-API-Key"
INVALID_OR_MISSING_API_KEY = "API key is invalid or is missing."


def check_api_key(**func_param):
    """
    A decorator to validate the API key in the request header.

    This decorator checks if the API key provided in the request header matches the expected API key.
    If the API key is valid, the decorated function is executed; otherwise, an AttributeError is raised.

    Parameters:
    -----------
    **func_param : dict
        A dictionary containing:
        - 'REQUEST_FROM_ENDPOINT': The request object from which the API key is extracted.
        - 'APP_API_KEY': The expected API key to validate against.

    Raises:
    -------
    AttributeError:
        If the API key is missing or does not match the expected value.
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
