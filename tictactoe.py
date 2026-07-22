#!/usr/bin/env python3
"""Terminal-based two-player Tic Tac Toe. No AI — just two humans taking turns."""

import sys


# Board cells are indexed 0..8, laid out row by row:
#   0 | 1 | 2
#   ---------
#   3 | 4 | 5
#   ---------
#   6 | 7 | 8
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]

EMPTY = " "
PLAYERS = ("X", "O")


def new_board():
    """Return a fresh board with every cell empty."""
    return [EMPTY] * 9


def render_board(board):
    """Return a human-readable string for the current board."""
    rows = []
    for r in range(3):
        cells = [board[r * 3 + c] for c in range(3)]
        rows.append(" {} | {} | {} ".format(*cells))
    separator = "-----------"
    return "\n {} \n".format(separator).join(rows)


def available_moves(board):
    """Return the 1-based positions of empty cells."""
    return [i + 1 for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board):
    """Return the winning mark, or None if there is no winner yet."""
    for a, b, c in WINNING_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    """Return True if the board has no empty cells left."""
    return all(cell != EMPTY for cell in board)


def prompt_move(board, player):
    """Ask the current player for a move. Loops until a legal move is entered."""
    while True:
        raw = input("Player {}, enter your move (1-9): ".format(player)).strip()
        if raw.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            sys.exit(0)
        if not raw.isdigit():
            print("Please enter a number between 1 and 9, or 'q' to quit.")
            continue
        pos = int(raw)
        if pos < 1 or pos > 9:
            print("That's off the board. Choose 1 through 9.")
            continue
        idx = pos - 1
        if board[idx] != EMPTY:
            print("That cell is already taken. Pick another.")
            continue
        return idx


def play_game():
    """Run a single game of Tic Tac Toe and print the result."""
    board = new_board()
    turn = 0

    print("Welcome to Tic Tac Toe!")
    print("Enter a number 1-9 to place your mark in that cell.")
    print("Type 'q' at any time to quit.\n")

    while True:
        player = PLAYERS[turn % 2]
        print("\n" + render_board(board))
        move = prompt_move(board, player)
        board[move] = player

        winner = check_winner(board)
        if winner is not None:
            print("\n" + render_board(board))
            print("\nPlayer {} wins! Congratulations!".format(winner))
            return

        if is_full(board):
            print("\n" + render_board(board))
            print("\nIt's a draw!")
            return

        turn += 1


def main():
    """Entry point: play rounds until the user quits."""
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    main()
