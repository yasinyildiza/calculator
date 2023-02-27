# Calculator

A simple calculator as a project sample.

# Setup

## Poetry

The project uses poetry for dependency management, so first install poetry:

`curl -sSL https://install.python-poetry.org | python3 -`

Then, ensure the installation is done properly by checking poetry version:

`poetry --version`

For more information about poetry, refer to the (official website)[https://python-poetry.org/].

## Python Version

The project uses Python3.10, so it must be installed along with poetry. Refer to (python.org)[https://python.org] for instrustions.

Once you have Pyhton3.10 installed in your environment, tell poetry to use it:

`poetry env use python3.10`

Note that poetry will try to find the appropriate Python version from the environment based on pyproject.toml file, but as they say:

> Explicit is better than implicit.

## Virtual Environment

Poetry will take care of managing the virtual environment. Just run the folloiwng command:

`poetry install`

# Local run

Run the following command to start the Flask application:

`poetry run python manage.py runserver`

Then, go to http://localhost:5000/status.

# Unit tests

`poetry run pytest`
