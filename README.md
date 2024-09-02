
# My Utility Package

## Overview
The `my_utility_package` provides essential utilities for managing API key validation, handling dummy responses, and managing configurations and database connections. This package includes the following components:

1. **check_api_key** - A decorator to validate API keys in request headers.
2. **conditioned_dummy_response** - A decorator to return a dummy response based on a condition.
3. **ConfigLoader** - A class to load and manage application configurations from environment variables and AWS Secrets Manager.
4. **DatabaseConnection** - A class to manage database connections and reflect database tables.

## Installation

To install the package, simply clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/my_utility_package.git
cd my_utility_package
pip install -r requirements.txt
```

## Usage

### 1. check_api_key

The `check_api_key` decorator is used to validate the presence and correctness of an API key in the request header. If the API key is valid, the decorated function is executed.

```python
from my_utility_package import check_api_key
from flask import request

APP_API_KEY = "your_expected_api_key"

@check_api_key(REQUEST_FROM_ENDPOINT=request, APP_API_KEY=APP_API_KEY)
def protected_endpoint():
    return {"message": "Access granted!"}, 200
```

### 2. conditioned_dummy_response

The `conditioned_dummy_response` decorator is used to return a predefined dummy response when a certain condition is met.

```python
from my_utility_package import conditioned_dummy_response

@conditioned_dummy_response(DUMMY_ACTIVE=True, DUMMY_RESPONSE={"message": "This is a dummy response"})
def my_route_function():
    return {"message": "Real response"}, 200
```

### 3. ConfigLoader

The `ConfigLoader` class is used to load configurations from a `.env` file and AWS Secrets Manager.

```python
from my_utility_package import ConfigLoader

config_loader = ConfigLoader(config_file=".env")
configurations = config_loader.configurations
print(configurations)
```

### 4. DatabaseConnection

The `DatabaseConnection` class is used to manage database connections and reflect database tables.

```python
from my_utility_package import DatabaseConnection

app_config = {
    "DRIVER": "postgresql",
    "USER": "your_db_user",
    "PASSWORD": "your_db_password",
    "HOST": "localhost",
    "PORT": "5432",
    "DATABASE": "your_database_name",
    "TIMEOUT": "10"
}

db_conn = DatabaseConnection(app_config=app_config)
engine = db_conn.get_engine()
session = db_conn.get_session()
metadata = db_conn.get_metadata()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
