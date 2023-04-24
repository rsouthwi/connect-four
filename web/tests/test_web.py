import json

from .conftest import client


def test_root_path__returns_200_response(client):
    response = client.get("/")
    assert response.status_code == 200


def test_c4_path__returns_200_response(client):
    response = client.get("/c4")
    assert response.status_code == 200


def test_traffic_to_unknown_path__redirected(client):
    response = client.get("/gibberish")
    assert response.status_code == 302


def test_traffic_to_unknown_path__redirected_to_root_404_page(client):
    response = client.get("/gibberish")
    assert response.location == "https://www.ronsouthwick.com/404.html"


def test_post_to_continue_game__returns_200(client):
    # Arrange
    board = {"A": [None, None, None, None, None, None],
             "B": [None, None, None, None, None, None],
             "C": [None, None, None, None, None, None],
             "D": [1, None, None, None, None, None],
             "E": [None, None, None, None, None, None],
             "F": [None, None, None, None, None, None],
             "G": [None, None, None, None, None, None]}
    # Act
    response = client.post("/c4", data={"board_state": json.dumps({"board": board,
                                                                   "player_turn": 2,
                                                                   "player_selected_column": 0})})
    # Assert
    assert response.status_code == 200


def test_post_to_continue_game__returns_updated_board(client):
    # Arrange
    board = {"A": [None, None, None, None, None, None],
             "B": [None, None, None, None, None, None],
             "C": [None, None, None, None, None, None],
             "D": [1, None, None, None, None, None],
             "E": [None, None, None, None, None, None],
             "F": [None, None, None, None, None, None],
             "G": [None, None, None, None, None, None]}
    # Act: player 2 selects column 0 and now should be in the bottom row of that column
    response = client.post("/c4", data={"board_state": json.dumps({"board": board,
                                                                   "player_turn": 2,
                                                                   "player_selected_column": 0})})
    # Assert the board state has player two in the bottom row of column 0
    assert b'"board": {"A": [2' in response.data
