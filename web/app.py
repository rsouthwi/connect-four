from flask import Flask, redirect, render_template, request
import json
from markupsafe import Markup

from game.exceptions import ColumnFullException
from game.models import ConnectFourBoard, BoardState

app = Flask(__name__)
app.url_map.strict_slashes = False


def render_game_board(board_state: BoardState) -> str:
    board = board_state.get("board")
    board_height = len(board.get("A"))
    players = ["◯", "\x1b[31m●\x1b[0m", "●"]
    output = "&nbsp;┌––––––––––––––––––––––┐<br />"
    for i in range(board_height-1, -1, -1):
        output += "&nbsp;|"
        for column, row in board.items():
            slot = players[row[i]] if row[i] is not None else "_"
            output += f"|{slot}&nbsp;"
        output += "||<br />"
    output += "&nbsp;|┕━━━━━━━━━━━━━━━━━━━━┙|<br />"
    output += """╱╱ <span id='col_0' class='col'>A</span> &nbsp;<span id='col_1' class='col'>B</span>
     &nbsp;<span id='col_2' class='col'>C</span> &nbsp;<span id='col_3' class='col'>D</span>
     &nbsp;<span id='col_4' class='col'>E</span> &nbsp;<span id='col_5' class='col'>F</span> 
     &nbsp;<span id='col_6' class='col'>G</span> &nbsp;╲╲"""
    output = output.replace("\x1b[31m●\x1b[0m", "<span style='color: red;'>●</span>")
    return Markup(output)


@app.get("/c4")
@app.get("/")
def start_game():
    fresh_board = ConnectFourBoard()
    board_state = BoardState(board=fresh_board.board, player_turn=fresh_board.current_player)
    markup = render_game_board(board_state)
    data = {
        "board": markup,
        "board_state": json.dumps(board_state),
        "game_over": False,
        "message": Markup(f"&nbsp;&nbsp;It's Player{fresh_board.current_player}'s turn...")
    }
    return render_template("base.html", **data)


@app.post("/c4")
@app.post("/")
def continue_game():
    board_string = request.form['board_state']
    previous_state = BoardState(**json.loads(board_string))
    try:
        in_progress_game = ConnectFourBoard(board_state=previous_state)
    except ColumnFullException:
        message = f"Invalid move: Column Full.<br /> &nbsp;&nbsp;It's player{previous_state['player_turn']}'s turn..."
        data = {
            "board": render_game_board(previous_state),
            "message": Markup(message),
            "board_state": json.dumps(previous_state)
        }
        return render_template("base.html", **data)
    if not in_progress_game.game_over:
        if in_progress_game.board_full:
            message = Markup("The board is full. Tie game. <br /><a href>Play again</a>?")
            data = {
                "board": render_game_board(previous_state),
                "message": Markup(message),
                "board_state": json.dumps(previous_state)
            }
            return render_template("base.html", **data)
        in_progress_game.switch_player_turns()
        message = Markup(f"&nbsp;&nbsp;It's Player{in_progress_game.current_player}'s turn...")
        game_over = False
    else:
        message = Markup(f"&nbsp;&nbsp;The winner is Player{in_progress_game.current_player}!"
                         f"<br /><a href>Play again</a>?")
        game_over = True
    current_state = BoardState(board=in_progress_game.board, player_turn=in_progress_game.current_player)
    markup = render_game_board(current_state)
    data = {
        "board": markup,
        "board_state": json.dumps(current_state),
        "game_over": game_over,
        "message": message
    }
    return render_template("base.html", **data)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("https://www.ronsouthwick.com/404.html", code=302)
