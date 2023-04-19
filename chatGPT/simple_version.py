# When prompted for ChatGPT to:
"""
Connect Four is a game where you and another player take turns placing checkers into a 7x6 board
trying to get four in a row while preventing your opponent from doing the same.
The game Connect Four is played by two players taking turns dropping a red or black piece
into one of the columns. When there are four of one color in a straight line (including diagonals),
that player wins.  Create a python script for a playable game of Connect Four.
"""
# Here's what it spit out:
# Connect Four
# By [Your Name]

# Define the game board
BOARD_ROWS = 6
BOARD_COLS = 7


# Print the game board
def print_board(board):
    print('--------------------')
    for row in board:
        print('|', end='')
        for col in row:
            if col == 0:
                print(' ', end='|')
            elif col == 1:
                print('X', end='|')
            else:
                print('O', end='|')
        print()
    print('--------------------')


# Check if a player has won
def check_winner(board, player):
    # Check rows
    for row in board:
        if row.count(player) == 4:
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if [board[row][col] for row in range(BOARD_ROWS)].count(player) == 4:
            return True
    # Check diagonals
    for col in range(BOARD_COLS - 3):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and \
                    board[row + 3][col + 3] == player:
                return True
    for col in range(BOARD_COLS - 3):
        for row in range(3, BOARD_ROWS):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and \
                    board[row - 3][col + 3] == player:
                return True
    # No winner yet
    return False


# Play the game
def play_game():
    # Create the game board
    board = [[0 for col in range(BOARD_COLS)] for row in range(BOARD_ROWS)]

    # Start with player 1
    turn = 1

    # Loop until there is a winner or the board is full
    while True:
        print_board(board)

        # Prompt the player for their move
        col = int(input('Player ' + str(turn) + ', choose a column (1-7): ')) - 1

        # Find next available row in the selected column
        for row in range(BOARD_ROWS - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = turn
                break
        else:
            print('Column is full, choose another column')
            continue

        # Check if the player has won
        if check_winner(board, turn):
            print_board(board)
            print('Player ' + str(turn) + ' wins!')
            break

        # Check if the board is full
        if all([col != 0 for row in board for col in row]):
            print_board(board)
            print('The game is a draw.')
            break

        # Switch to the next player
        turn = 1 if turn == 2 else 2


# Call the play_game function to start the game
# play_game()