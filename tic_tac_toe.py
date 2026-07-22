"""Tic Tac Toe — terminal entry point.

Run this file directly to play a two-player game in the terminal::

    python tic_tac_toe.py

The game reuses the :class:`board.Board` class, so all board rules live in one
place and this module only handles turns, input, flow control, and scorekeeping.

Across a single session the players keep their names and symbols; a scoreboard
tracks wins for each player and the number of draws, printed after every game.
"""

from __future__ import annotations

import sys
from typing import Dict, Tuple

from board import Board


def two_player_game(names: Tuple[str, str], scoreboard: "Scoreboard") -> None:
    """Run a single two-player game of Tic Tac Toe and update the scoreboard.

    ``names`` is the ``(X_name, O_name)`` pair established at the start of the
    session, so players do not re-enter their names between rounds. ``scoreboard``
    is the mutable :class:`Scoreboard` instance for the session; it is updated
    once the game ends and then printed so the players can see the running totals.

    Player ``X`` always moves first. On each turn the board is shown, the current
    player is prompted for a cell number (1–9), and the move is applied through
    :meth:`board.Board.make_move`. Invalid input is rejected and the turn is not
    advanced.

    The loop ends as soon as :meth:`board.Board.is_game_over` is true. A win is
    announced with the victor's name and symbol; a full board with no winner is
    a draw. In either case the scoreboard is credited before returning so the
    caller can display the updated totals.
    """
    board = Board()
    symbols: Tuple[str, str] = ("X", "O")
    turn: int = 0  # even turns are names[0]/X, odd turns are names[1]/O

    while True:
        symbol = symbols[turn % 2]
        name = names[turn % 2]
        board.display()
        print()

        move = _prompt_player_move(board, name)
        board.make_move(move, symbol)

        if board.winner() is not None:
            print()
            board.display()
            print("\n{} ({}) wins!".format(name, symbol))
            scoreboard.record_win(symbol)
            break

        if board.is_full():
            print()
            board.display()
            print("\nIt's a draw!")
            scoreboard.record_draw()
            break

        turn += 1


def _prompt_player_names() -> Tuple[str, str]:
    """Ask both players for their names and return them as ``(X_name, O_name)``.

    Empty input is rejected so every player has a visible name to display during
    the game and on the scoreboard. The first name entered is assigned to player
    ``X`` (who always moves first) and the second to player ``O``.
    """
    names: list[str] = []
    symbols: Tuple[str, str] = ("X", "O")
    for symbol in symbols:
        while True:
            raw = input("Enter the name for player {}: ".format(symbol)).strip()
            if raw:
                names.append(raw)
                break
            print("Please enter a non-empty name.")
    return tuple(names)


def _prompt_player_move(board: Board, name: str) -> int:
    """Ask the player called ``name`` for a move and return a validated 0-based index.

    The player types a number from 1 to 9, where 1 is the top-left cell and 9
    is the bottom-right. The value is converted to a 0-based index for the
    :class:`board.Board`. The special inputs ``q``, ``quit`` and ``exit`` quit
    the program immediately so a player is never forced to make a move.

    Validation happens in stages so the error message matches the actual problem
    instead of giving a single generic rejection:

    * non-numeric input is rejected outright, before any numeric conversion;
    * numbers outside 1–9 are off the board and cannot map to a cell;
    * numbers pointing at an already-occupied cell are rejected so a player
      cannot overwrite an existing mark, even their own.

    Any rejected input leaves the turn unchanged and the question is asked again.
    """
    while True:
        raw = input("{}, choose your move (1-9): ".format(name)).strip()

        # Allow the player to quit at any prompt instead of forcing a move.
        if raw.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            sys.exit(0)

        # Reject anything that is not a plain integer before doing numeric work,
        # so negative numbers, decimals and free text all get a clear message.
        if not raw.isdigit():
            print("Please enter a number between 1 and 9, or 'q' to quit.")
            continue

        pos = int(raw)

        # The board only has cells 1 through 9; anything else is out of range.
        if pos < 1 or pos > 9:
            print("{}, that number is off the board. Choose 1 through 9.".format(name))
            continue

        index = pos - 1

        # A move must land on an empty cell; overwriting is never allowed.
        if board.cells[index] != " ":
            print("{}, that cell is already taken. Pick an empty one.".format(name))
            continue

        return index


class Scoreboard:
    """Tracks wins for each symbol and draws across a multi-round session.

    The scoreboard lives for the whole session so that scores accumulate from
    game to game. It stores counts keyed by symbol (``"X"`` and ``"O"``) plus a
    separate draw counter. :meth:`record_win`, :meth:`record_draw` and
    :meth:`display` are the only public ways to touch the counts, so the data
    cannot be corrupted by accident and the per-symbol / per-draw distinction
    stays consistent.
    """

    def __init__(self) -> None:
        """Start a fresh scoreboard with every count at zero."""
        self.wins: Dict[str, int] = {"X": 0, "O": 0}
        self.draws: int = 0

    def record_win(self, symbol: str) -> None:
        """Credit a win to ``symbol`` (``"X"`` or ``"O"``)."""
        self.wins[symbol] += 1

    def record_draw(self) -> None:
        """Credit a draw to the session total."""
        self.draws += 1

    def display(self, names: Tuple[str, str]) -> None:
        """Print the current scores, labeled with the players' names.

        ``names`` must be the ``(X_name, O_name)`` pair for the session so each
        line can show the player's name alongside their symbol. This is called
        after every game so the players see the running totals before deciding
        whether to play another round.
        """
        print("\nScoreboard:")
        print("  {} (X): {}".format(names[0], self.wins["X"]))
        print("  {} (O): {}".format(names[1], self.wins["O"]))
        print("  Draws:  {}".format(self.draws))


def play_again() -> bool:
    """Ask whether the players want another game and return ``True`` if they do.

    Accepts ``y`` or ``yes`` (case-insensitive) as a positive answer; anything
    else is treated as a refusal. This keeps the prompt strict so accidental
    keystrokes do not start an unwanted new game.
    """
    answer = input("\nPlay again? (y/n): ").strip().lower()
    return answer in ("y", "yes")


def main() -> None:
    """Entry point: run a session of games with a shared scoreboard.

    Player names are collected once at the start and reused for every round, so
    the scoreboard can attribute wins to the same two players throughout the
    session. After each game the score is shown and the players choose whether
    to play again. The loop only terminates when the players decline or quit.
    """
    names = _prompt_player_names()
    scoreboard = Scoreboard()

    print("\n{} is X and {} is O. {} goes first.".format(
        names[0], names[1], names[0]))

    while True:
        two_player_game(names, scoreboard)
        scoreboard.display(names)
        if not play_again():
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    main()
