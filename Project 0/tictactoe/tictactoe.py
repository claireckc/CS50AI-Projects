"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def get_empty_count(board):
    count = 0
    for outer in board:
        for inner in outer:
            count += inner == EMPTY
    return count

def player(board):

    """
    Returns player who has the next turn on a board. (either X or O)
    initial state (check if board is empty): X
    initial state can also be if empty count is 9
    but also means solution is not scalable, but lets assume its always going to be 3 by 3 grid
    each additional move, if board still has an empty spot, (odd: X, even: O)
    """

    # In the initial game state, X gets the first move.
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    # odd count: X, even count: O
    if board == initial_state() or terminal(board) or get_empty_count(board) % 2 == 1:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board. 
    i = row, j corresponds which cell in row
    possible moves cell should not have any X or O in them, aka must be EMPTY
    """
    actions = set()
    # all possible moves would be cells with EMPTY in it
    for row, outer in enumerate(board):
        for col, inner in enumerate(outer):
            if inner == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    return new board without modifying original board (deep copy of board first)
    action invalid? raise exception
    return original board + action
    """
    # validate action
    if len(action) != 2:
        raise Exception("Invalid action")

    row = action[0]
    col = action[1]

    if board[row][col] != EMPTY:
        raise Exception("Invalid action")
    
    # update board
    updatedBoard = [row[:] for row in board]
    updatedBoard[row][col] = player(board)

    return updatedBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    win criteria: horizontal, vertical or diagonal 3 consecutive shape
    no winner: None
    """
    # check horizontal
    for i, _ in enumerate(board):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    # check vertical
    for i, _ in enumerate(board):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # check diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    board is filled: true else false
    """
    if get_empty_count(board) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Max: X
    Min: -1
    Tie: 0
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    if winner_player == O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None
    """
    Returns the optimal action for the current player on the board.
    if multiple moves are equally optimal: return any of them
    """
    turn = player(board)
    bestMove = None
    currentMax = -1
    currentMin = 1
    if turn == X:
        """
        get initial actions
        only from each initial actions, do we find the max utility
        then we choose the action from the max utility
        """
        for a in actions(board):
            min_util = get_min_utility(result(board, a))
            if currentMax < min_util :
                currentMax = min_util
                bestMove = a

        return bestMove
    if turn == O:
        for a in actions(board):
            max_util = get_max_utility(result(board, a))
            if currentMin > max_util :
                currentMin = max_util
                bestMove = a

        return bestMove

    # return any possible action
    return actions(board).pop()

# returns int, action
def get_max_utility(board):
    # since the least value is -1, we will use that
    currentMax = -1
    bestActions = set()
    if terminal(board):
        return utility(board)
    for action in actions(board):
        currentMax = max(currentMax, get_min_utility(result(board, action)))
    return currentMax


def get_min_utility(board):
    # since the largest value is 1, we will use that
    currentMin = 1
    if terminal(board):
        return utility(board)
    for action in actions(board):
        currentMin = min(currentMin, get_max_utility(result(board, action)))
    return currentMin