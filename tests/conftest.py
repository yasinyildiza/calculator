import pytest

import calculator


@pytest.fixture
def app():
    yield calculator.create_app(
        config_override={
            "DEBUG": True,
            "TESTING": True,
        }
    )


@pytest.fixture
def test_client(app):
    yield app.test_client()
