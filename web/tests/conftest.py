import pytest
from web.app import app as c4


@pytest.fixture()
def app():
    c4.config.update({
        "TESTING": True,
    })
    yield c4


@pytest.fixture()
def client():
    c4.config.update({
        "TESTING": True,
    })
    with c4.test_client() as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
