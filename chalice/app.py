import json
import os
from typing import Dict
from urllib.parse import parse_qs

from chalice import Chalice, Response
import jinja2
from markupsafe import Markup

from chalicelib.exceptions import ColumnFullException
from chalicelib.models import BoardState, ConnectFourBoard

app = Chalice(app_name='c4')


@app.route('/test')
def index():
    return {'hello': 'world'}


@app.route("/", methods=['GET'])
def start_game() -> Response:
    fresh_board = ConnectFourBoard()
    board_state = BoardState(board=fresh_board.board, player_turn=fresh_board.current_player)
    data = {
        "game_over": False,
        "message": Markup(f"&nbsp;&nbsp;It's Player{fresh_board.current_player}'s turn...")
    }
    return render_game_board(board_state, data)


@app.route("/", methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def continue_game():
    parsed = parse_qs(app.current_request.raw_body.decode())
    board_string = parsed.get('board_state')[0]
    previous_state = BoardState(**json.loads(board_string))
    try:
        in_progress_game = ConnectFourBoard(board_state=previous_state)
    except ColumnFullException:
        message = f"Invalid move: Column Full.<br /> &nbsp;&nbsp;It's player{previous_state['player_turn']}'s turn..."
        return render_game_board(previous_state, {"message": Markup(message)})
    if not in_progress_game.game_over:
        if in_progress_game.board_full:
            message = Markup("The board is full. Tie game. <br /><a href>Play again</a>?")
            game_over = True
        else:
            in_progress_game.switch_player_turns()
            message = Markup(f"&nbsp;&nbsp;It's Player{in_progress_game.current_player}'s turn...")
            game_over = False
    else:
        message = Markup(f"&nbsp;&nbsp;The winner is Player{in_progress_game.current_player}!"
                         f"<br /><a href>Play again</a>?")
        game_over = True
    current_state = BoardState(board=in_progress_game.board, player_turn=in_progress_game.current_player)
    data = {
        "game_over": game_over,
        "message": message
    }
    return render_game_board(current_state, data)


def redirect(url, code=301) -> Response:
    return Response(status_code=code, headers={'Location': url}, body='')


def render(tpl_path: str, context: Dict[str, str]) -> str:
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(context)


def render_game_board(board_state: BoardState, data: Dict) -> Response:
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
    game_board = Markup(output)
    data['board'] = game_board
    data['board_state'] = json.dumps(board_state)
    template = render("chalicelib/templates/base.html", data)
    return Response(template, status_code=200,
                    headers={"Content-Type": "text/html",
                             "Access-Control-Allow-Origin": "*"}
                    )
