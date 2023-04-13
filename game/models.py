from typing import Union, Optional, List, Dict, TypedDict

from .exceptions import ColumnFullException

"""
this is where we can articulate a "board".  in case the app is stateless,
the board will need to be able to:
    - start a new game from scratch, creating an empty board
    - construct a board from the middle of a game
    - allow a user to be specified on instantiation
    - process any logic around setting a piece
    - process any logic to determine if the game is over
    
"""


class BoardState(TypedDict):
    player_turn: int
    player_selected_column: Optional[int]
    board: Dict[str, List[Union[int, None]]]


class ConnectFourBoard:
    board = {}
    board_height = 6
    columns = ["A", "B", "C", "D", "E", "F", "G"]
    current_player = 1
    game_over = False
    winner = None

    def __init__(self, board_state: Optional[BoardState] = None) -> None:
        if board_state:
            self.board = board_state.get("board")
            self.current_player = board_state.get("player_turn")
            selected_column_index = board_state.get("player_selected_column")
            column_key = self.columns[selected_column_index]
            piece_row = self.set_piece(column_key, self.current_player)
            if self.did_player_win(self.current_player, column_key, piece_row):
                self.game_over = True
                self.winner = self.current_player
        else:
            self._set_up_board()

    @property
    def board_full(self) -> bool:
        for column in self.columns:
            if None in self.board[column]:
                return False
        return True

    def _set_up_board(self) -> None:
        for column in self.columns:
            self.board[column] = [None for i in range(self.board_height)]

    def set_piece(self, column: str, player: int) -> int:
        """
        :param column: str
        :param player: int
        :return: the index of the row where the piece fell
        """
        selected_column = self.board[column]
        for idx, slot in enumerate(selected_column):
            if slot is None:
                selected_column[idx] = player
                return idx
        raise ColumnFullException

    def did_player_win(self, player: int, column_key: str, row_index: int) -> bool:
        row_group = self._get_row_group(row_index)
        column_group = self._get_column_group(column_key)
        diagonal_down = self._get_descending_diagonal_group(column_key, row_index)
        diagonal_up = self._get_ascending_diagonal_group(column_key, row_index)
        ways_to_win = (row_group, column_group, diagonal_down, diagonal_up)

        for group in ways_to_win:
            if self._check_result(player, group):
                return True
        return False

    def switch_player_turns(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    @staticmethod
    def _check_result(player: int, piece_group: List) -> bool:
        slot_streak = 0
        for slot in piece_group:
            if slot == player:
                slot_streak += 1
                if slot_streak == 4:
                    return True
            else:
                slot_streak = 0
        return False

    def _get_row_group(self, row_index: int) -> List[int]:
        return [column[row_index] for column in self.board.values()]

    def _get_column_group(self, column_key: str) -> List[int]:
        return self.board.get(column_key)

    def _get_descending_diagonal_group(self, column_key: str, row_index: int) -> List[int]:
        diagonal_desc = []
        columns = list(self.board.keys())

        # considering the row index and column,
        # climb up and to the left to find the start of the run
        group_column_index = columns.index(column_key)
        group_row_index = row_index
        while group_column_index > 0 and group_row_index < self.board_height - 1:
            group_column_index -= 1
            group_row_index += 1
        for col in columns[group_column_index:]:
            diagonal_desc.append(self.board[col][group_row_index])
            if group_row_index == 0:
                break
            group_row_index -= 1

        return diagonal_desc

    def _get_ascending_diagonal_group(self, column_key: str, row_index: int) -> List[int]:
        diagonal_asc = []
        columns = list(self.board.keys())

        # climb down and to the left to find the start of the run
        group_column_index = columns.index(column_key)
        group_row_index = row_index
        while group_column_index > 0 and group_row_index > 0:
            group_column_index -= 1
            group_row_index -= 1
        for col in columns[group_column_index:]:
            diagonal_asc.append(self.board[col][group_row_index])
            if group_row_index == self.board_height - 1:
                break
            group_row_index += 1
        return diagonal_asc
