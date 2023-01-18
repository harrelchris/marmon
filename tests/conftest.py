import pytest


@pytest.fixture
def app():
    app = None

    # setup

    yield app

    # teardown
