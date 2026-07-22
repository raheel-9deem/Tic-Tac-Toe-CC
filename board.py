"""Board representation for Tic Tac Toe.

The board is a list of 9 cells indexed 0 through 8, laid out row by row:

    0 | 1 | 2
    ----------
    3 | 4 | 5
    ----------
    6 | 7 | 8

An empty cell holds a single space " ", and an occupied cell holds "X" or "O".
"""


class Board:
    """Holds the state of a Tic Tac Toe game and the rules for playing on it."""

    # Every triple of indices that counts as a win: rows, columns, diagonals.
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def __init__(self):
        """Create a fresh empty board."""
        self.cells = [" "] * 9

    def display(self):
        """Print the board as a readable grid to the terminal."""
        for row in range(3):
            start = row * 3
            a, b, c = self.cells[start], self.cells[start + 1], self.cells[start + 2]
            print(" {} | {} | {} ".format(a, b, c))
            if row < 2:
                print("-----------")

    def available_moves(self):
        """Return a list of the indices of empty cells.

        These are the legal moves a player may choose from on their turn.
        """
        return [i for i, cell in enumerate(self.cells) if cell == " "]

    def make_move(self, index, symbol):
        """Place ``symbol`` ("X" or "O") at ``index``.

        Raises ``ValueError`` if the index is off the board or the cell is
        already occupied, so callers do not need to validate separately.
        """
        if not 0 <= index <= 8:
            raise ValueError("Index must be between 0 and 8.")
        if self.cells[index] != " ":
            raise ValueError("Cell {} is already occupied.".format(index))
        self.cells[index] = symbol

    def winner(self):
        """Return the winning symbol ("X" or "O"), or None if there is none.

        Checks every winning line; the first line whose three cells all hold
        the same non-empty symbol determines the winner.
        """
        for a, b, c in self.WIN_LINES:
            cell = self.cells[a]
            if cell != " " and cell == self.cells[b] == self.cells[c]:
                return cell
        return None

    def is_full(self):
        """Return True if every cell is occupied, False otherwise."""
        return all(cell != " " for cell in self.cells)

    def is_game_over(self):
        """Return True when the game should end.

        The game is over once there is a winner or the board is full (a draw).
        """
        return self.winner() is not None or self.is_full()

    def reset(self):
        """Clear the board back to an empty state for a new game."""
        self.cells = [" "] * 9
