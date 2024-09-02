from functools import wraps


def conditioned_dummy_response(**func_param):
    """
    A decorator that returns a dummy response if a specified condition is met.

    This decorator checks if dummy mode is active (as specified by the `DUMMY_ACTIVE` parameter).
    If dummy mode is active, it returns a predefined dummy response with a 200 status code.
    Otherwise, it proceeds to execute the original route function.

    Parameters:
    -----------
    **func_param : dict
        A dictionary containing:
        - 'DUMMY_ACTIVE': A boolean indicating whether dummy mode is active.
        - 'DUMMY_RESPONSE': The response to return if dummy mode is active.

    Returns:
    --------
    Response tuple
        If dummy mode is active, returns the `DUMMY_RESPONSE` with a 200 status code.
        Otherwise, returns the original function's response.
    """
    def decorator(route_func):
        @wraps(route_func)
        def wrapper(*args, **kwargs):
            dummy_mode = func_param["DUMMY_ACTIVE"]
            if dummy_mode:
                dummy_response = func_param["DUMMY_RESPONSE"]
                return dummy_response, 200
            return route_func(*args, **kwargs)

        return wrapper

    return decorator
