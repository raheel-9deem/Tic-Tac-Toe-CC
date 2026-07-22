"""Board representation for Tic Tac Toe.

The board is a list of 9 cells indexed 0 through 8, laid out row by row::

    0 | 1 | 2
    ----------
    3 | 4 | 5
    ----------
    6 | 7 | 8

An empty cell holds a single space ``" "``, and an occupied cell holds ``"X"``
or ``"O"``. This module owns the rules of the game; the entry point in
:mod:`tic_tac_toe` only handles turns, input, and flow control.
"""

from __future__ import annotations

from typing import List, Optional, Tuple


class Board:
    """Holds the state of a Tic Tac Toe game and the rules for playing on it.

    The public API is intentionally small: create a board, apply moves through
    :meth:`make_move`, query the result with :meth:`winner` / :meth:`is_full` /
    :meth:`is_game_over`, and call :meth:`reset` to reuse the instance for a
    fresh game. The raw ``cells`` list is exposed for read-only inspection and
    for the tests, but callers should not mutate it directly.
    """

    # Every triple of indices that counts as a win: three rows, three columns,
    # and the two diagonals. Adding or removing a line here is the only change
    # needed to alter the winning conditions.
    WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    )

    def __init__(self) -> None:
        """Create a fresh empty board ready for a new game."""
        self.cells: List[str] = [" "] * 9

    def display(self) -> None:
        """Print the board as a human-readable grid to the terminal.

        Each cell is printed as-is, so empty cells show as blank space while
        occupied cells show their mark. Rows are separated by a dashed line to
        keep the 3x3 structure visually clear.
        """
        for row in range(3):
            start = row * 3
            a, b, c = self.cells[start], self.cells[start + 1], self.cells[start + 2]
            print(" {} | {} | {} ".format(a, b, c))
            if row < 2:
                print("-----------")

    def available_moves(self) -> List[int]:
        """Return a list of the indices of empty cells.

        These are the legal moves a player may choose from on their turn. The
        returned indices are 0-based, matching the internal board layout; the
        entry point converts them to 1-based numbers for display and input.
        """
        return [i for i, cell in enumerate(self.cells) if cell == " "]

    def make_move(self, index: int, symbol: str) -> None:
        """Place ``symbol`` (``"X"`` or ``"O"``) at ``index``.

        The index must be between 0 and 8 inclusive, and the target cell must be
        empty. Violating either condition raises ``ValueError`` so callers do
        not need to validate separately before attempting a move.
        """
        if not 0 <= index <= 8:
            raise ValueError("Index must be between 0 and 8, got {}.".format(index))
        if self.cells[index] != " ":
            raise ValueError("Cell {} is already occupied by {!r}.".format(
                index, self.cells[index]))
        self.cells[index] = symbol

    def winner(self) -> Optional[str]:
        """Return the winning symbol (``"X"`` or ``"O"``), or ``None`` if there is none.

        Every winning line is checked in order; the first line whose three cells
        all hold the same non-empty symbol determines the winner. If no line is
        complete, the game has no winner yet.
        """
        for a, b, c in self.WIN_LINES:
            cell = self.cells[a]
            if cell != " " and cell == self.cells[b] == self.cells[c]:
                return cell
        return None

    def is_full(self) -> bool:
        """Return ``True`` if every cell is occupied, ``False`` otherwise.

        A full board with no winner is a draw. This does not by itself mean the
        game is over, since a win can occur before the board is full.
        """
        return all(cell != " " for cell in self.cells)

    def is_game_over(self) -> bool:
        """Return ``True`` when the game should end.

        The game is over as soon as there is a winner or the board is full (a
        draw). Callers can use this as the loop condition instead of checking
        both conditions separately.
        """
        return self.winner() is not None or self.is_full()

    def reset(self) -> None:
        """Clear the board back to an empty state for a new game.

        The same ``Board`` instance is reused rather than constructing a new
        one, which keeps references held by callers valid across rounds.
        """
        self.cells = [" "] * 9
