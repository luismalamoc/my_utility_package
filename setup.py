from setuptools import setup, find_packages

setup(
    name="my_utility_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",  # Add other dependencies if needed
    ],
    description="A utility package for common operations like sqlalchemy object connection, environment config loading, and dummy responses.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/my_utility_package",  # Optional
    author="Luis Alamo",
    author_email="luismauricioac@gmail.com",
    license="MIT",
)
