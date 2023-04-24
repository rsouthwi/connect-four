from .conftest import client


def test_root_path(client):
    response = client.get("/")
    assert response.status_code == 200


def test_c4_path(client):
    response = client.get("/c4")
    assert response.status_code == 200


def test_traffic_to_unknown_path_redirected(client):
    response = client.get("/gibberish")
    assert response.status_code == 302


def test_traffic_to_unknown_path_redirected_to_root_404_page(client):
    response = client.get("/gibberish")
    assert response.location == "https://www.ronsouthwick.com/404.html"
