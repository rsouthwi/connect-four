import pytest
from ..models import ConnectFourBoard, BoardState
from ..exceptions import ColumnFullException


class TestConnectFourBoard:
    def test_set_piece__with_empty_column__sets_piece(self):
        # Arrange
        board = ConnectFourBoard()
        # Act
        board.set_piece("A", 1)
        # Assert
        assert board.board["A"] == [1, None, None, None, None, None]

    def test_set_piece__with_full_column__raises_exception(self):
        # Arrange
        board = ConnectFourBoard()
        board.board["A"] = [1, 2, 1, 2, 1, 2]
        # Assert
        with pytest.raises(ColumnFullException):
            # Act
            board.set_piece("A", 1)

    def test_board_full_property__with_full_board__returns_true(self):
        # Arrange
        board = ConnectFourBoard()
        assert board.board_full is False
        board.board = {"A":[1, 2, 1, 2, 1, 2],
                       "B":[2, 2, 1, 1, 2, 2],
                       "C":[1, 1, 2, 2, 1, 1],
                       "D":[2, 1, 1, 1, 2, 2],
                       "E":[1, 2, 2, 2, 1, 1],
                       "F":[1, 2, 2, 2, 2, 1],
                       "G":[1, 2, 1, 2, 1, 1]}
        # Assert
        assert board.board_full is True

    def test_board_full_property__with_empty_board__returns_false(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[None, None, None, None, None, None],
                       "E":[None, None, None, None, None, None],
                       "F":[None, None, None, None, None, None],
                       "G":[None, None, None, None, None, None]}
        # Assert
        assert board.board_full is False

    def test_board_full_property__with_almost_full_board__returns_false(self):
        # Arrange
        board = ConnectFourBoard()
        assert board.board_full is False
        board.board = {"A":[1, 2, 1, 2, 1, 2],
                       "B":[2, 2, 1, 1, 2, 2],
                       "C":[1, 1, 2, 2, 1, 1],
                       "D":[2, 1, 1, 1, 2, None],
                       "E":[1, 2, 2, 2, 1, 1],
                       "F":[1, 2, 2, 2, 2, 1],
                       "G":[1, 2, 1, 2, 1, 1]}
        # Assert
        assert board.board_full is False

    def test_switch_player_turns__with_player_2__returns_player_1(self):
        # Arrange
        board = ConnectFourBoard()
        board.current_player = 2
        # Act
        board.switch_player_turns()
        # Assert
        assert board.current_player == 1

    def test_switch_player_turns__with_player_1__returns_player_2(self):
        # Arrange
        board = ConnectFourBoard()
        board.current_player = 1
        # Act
        board.switch_player_turns()
        # Assert
        assert board.current_player == 2

    def test_did_player_win__with_vertical_win__returns_true(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[None, None, None, None, None, None],
                       "E":[None, None, None, None, None, None],
                       "F":[None, None, None, None, None, None],
                       "G":[1, 1, 1, 1, None, None]}
        # Assert
        assert board.did_player_win(1, "G", 3) is True

    def test_did_player_win__with_horizontal_win__returns_true(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[1, None, None, None, None, None],
                       "E":[1, None, None, None, None, None],
                       "F":[1, None, None, None, None, None],
                       "G":[1, None, None, None, None, None]}
        # Assert
        assert board.did_player_win(1, "G", 0) is True

    def test_did_player_win__with_descending_diagonal_win__returns_true(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[1, 1, 1, 2, None, None],
                       "E":[1, 1, 2, None, None, None],
                       "F":[1, 2, None, None, None, None],
                       "G":[2, None, None, None, None, None]}
        # Assert
        assert board.did_player_win(2, "G", 0) is True

    def test_did_player_win__with_ascending_diagonal_win__returns_true(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[1, None, None, None, None, None],
                       "E":[2, 1, None, None, None, None],
                       "F":[1, 2, 1, None, None, None],
                       "G":[2, 2, 2, 1, None, None]}
        # Assert
        assert board.did_player_win(1, "D", 0) is True

    def test_did_player_win__with_no_win__returns_false(self):
        # Arrange
        board = ConnectFourBoard()
        board.board = {"A":[None, None, None, None, None, None],
                       "B":[None, None, None, None, None, None],
                       "C":[None, None, None, None, None, None],
                       "D":[1, 1, 1, 2, None, None],
                       "E":[1, 1, 1, None, None, None],
                       "F":[1, 2, None, None, None, None],
                       "G":[2, None, None, None, None, None]}
        # Assert
        assert board.did_player_win(2, "G", 0) is False

    def test_init__with_board_state__returns_board(self):
        # Arrange
        board_state = BoardState(
            board={"A": [2, None, None, None, None, None]},
            player_turn=1,
            player_selected_column=0
        )
        # Act
        board = ConnectFourBoard(board_state=board_state)

        # Assert
        assert board.board == {"A": [2, 1, None, None, None, None]}

#
#
# class ConnectFourBoard:
#     @property
#     def board_full(self) -> bool:
#         for column in self.columns:
#             if None in self.board[column]:
#                 return False
#         return True
#
#     def set_piece(self, column: str, player: int) -> int:
#         """
#         :param column: str
#         :param player: int
#         :return: the index of the row where the piece fell
#         """
#         selected_column = self.board[column]
#         for idx, slot in enumerate(selected_column):
#             if slot is None:
#                 selected_column[idx] = player
#                 return idx
#         raise ColumnFullException
#
#     def did_player_win(self, player: int, column_key: str, row_index: int) -> bool:
#         row_group = self._get_row_group(row_index)
#         column_group = self._get_column_group(column_key)
#         diagonal_down = self._get_descending_diagonal_group(column_key, row_index)
#         diagonal_up = self._get_ascending_diagonal_group(column_key, row_index)
#         ways_to_win = (row_group, column_group, diagonal_down, diagonal_up)
#
#         for group in ways_to_win:
#             if self._check_result(player, group):
#                 return True
#         return False
#
#     def switch_player_turns(self):
#         if self.current_player == 1:
#             self.current_player = 2
#         else:
#             self.current_player = 1
