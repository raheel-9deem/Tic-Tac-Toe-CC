"""Tests for the :class:`board.Board` class.

Run these with pytest from the project root::

    pytest tests/test_board.py

Each test covers a single behavior so a failure points directly at the rule
that regressed. The board uses 0-based indices laid out row by row::

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8
"""

import pytest

from board import Board


def _place_marks(board, marks):
    """Apply a sequence of ``(index, symbol)`` moves to ``board``.

    A small helper so each test reads as a list of moves rather than a loop of
    ``make_move`` calls.
    """
    for index, symbol in marks:
        board.make_move(index, symbol)


# -------------------------------------------------------------------------
# Fresh board state
# -------------------------------------------------------------------------

def test_new_board_is_empty():
    """A fresh board should have nine empty cells."""
    board = Board()
    assert board.cells == [" "] * 9
    assert board.available_moves() == list(range(9))


def test_new_board_has_no_winner():
    """A fresh board should not report a winner or a finished game."""
    board = Board()
    assert board.winner() is None
    assert not board.is_game_over()
    assert not board.is_full()


# -------------------------------------------------------------------------
# Win detection: rows
# -------------------------------------------------------------------------

def test_top_row_win():
    """Three marks across the top row (cells 0, 1, 2) should be a win."""
    board = Board()
    _place_marks(board, [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_middle_row_win():
    """Three marks across the middle row (cells 3, 4, 5) should be a win."""
    board = Board()
    _place_marks(board, [(0, "O"), (3, "X"), (1, "O"), (4, "X"), (5, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_bottom_row_win():
    """Three marks across the bottom row (cells 6, 7, 8) should be a win."""
    board = Board()
    _place_marks(board, [(0, "O"), (6, "X"), (1, "O"), (7, "X"), (8, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


# -------------------------------------------------------------------------
# Win detection: columns
# -------------------------------------------------------------------------

def test_left_column_win():
    """Three marks down the left column (cells 0, 3, 6) should be a win."""
    board = Board()
    _place_marks(board, [(0, "X"), (1, "O"), (3, "X"), (2, "O"), (6, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_middle_column_win():
    """Three marks down the middle column (cells 1, 4, 7) should be a win."""
    board = Board()
    _place_marks(board, [(1, "X"), (0, "O"), (4, "X"), (2, "O"), (7, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_right_column_win():
    """Three marks down the right column (cells 2, 5, 8) should be a win."""
    board = Board()
    _place_marks(board, [(2, "X"), (0, "O"), (5, "X"), (1, "O"), (8, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


# -------------------------------------------------------------------------
# Win detection: diagonals
# -------------------------------------------------------------------------

def test_top_left_to_bottom_right_diagonal_win():
    """The 0-4-8 diagonal should count as a win."""
    board = Board()
    _place_marks(board, [(0, "X"), (1, "O"), (4, "X"), (2, "O"), (8, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_top_right_to_bottom_left_diagonal_win():
    """The 2-4-6 diagonal should count as a win."""
    board = Board()
    _place_marks(board, [(2, "X"), (0, "O"), (4, "X"), (1, "O"), (6, "X")])
    assert board.winner() == "X"
    assert board.is_game_over()


def test_o_wins():
    """Win detection must work for both symbols, not just X.

    O takes the right column (cells 2, 5, 8) here, so the winner must be O
    regardless of X's scattered marks.
    """
    board = Board()
    _place_marks(board, [(0, "X"), (2, "O"), (1, "X"), (5, "O"), (3, "X"), (8, "O")])
    assert board.winner() == "O"
    assert board.is_game_over()


# -------------------------------------------------------------------------
# Draw detection
# -------------------------------------------------------------------------

def test_full_board_with_no_winner_is_draw():
    """A completely filled board with no winning line should be a draw.

    The arrangement below has marks from both players but no three-in-a-row.
    """
    board = Board()
    _place_marks(board, [
        (0, "X"), (1, "O"), (2, "X"),
        (3, "X"), (4, "O"), (5, "O"),
        (6, "O"), (7, "X"), (8, "X"),
    ])
    assert board.is_full()
    assert board.winner() is None
    assert board.is_game_over()


def test_partial_board_is_not_a_draw():
    """A board with empty cells and no winner should not be game over."""
    board = Board()
    _place_marks(board, [(0, "X"), (4, "O"), (8, "X")])
    assert not board.is_full()
    assert board.winner() is None
    assert not board.is_game_over()


# -------------------------------------------------------------------------
# Invalid move handling
# -------------------------------------------------------------------------

def test_out_of_range_index_raises():
    """An index below 0 or above 8 should raise ValueError."""
    board = Board()
    with pytest.raises(ValueError):
        board.make_move(-1, "X")
    with pytest.raises(ValueError):
        board.make_move(9, "X")


def test_occupied_cell_raises():
    """Playing in a cell that is already taken should raise ValueError."""
    board = Board()
    board.make_move(4, "X")
    with pytest.raises(ValueError):
        board.make_move(4, "O")


def test_overwriting_same_symbol_raises():
    """A player must not be able to overwrite even their own mark."""
    board = Board()
    board.make_move(0, "X")
    with pytest.raises(ValueError):
        board.make_move(0, "X")


# -------------------------------------------------------------------------
# available_moves() correctness
# -------------------------------------------------------------------------

def test_available_moves_on_empty_board():
    """Every cell index should be available on a fresh board."""
    board = Board()
    assert sorted(board.available_moves()) == list(range(9))


def test_available_moves_shrinks_as_cells_are_taken():
    """Occupied cells must drop out of available_moves, empty ones stay."""
    board = Board()
    board.make_move(0, "X")
    board.make_move(4, "O")
    board.make_move(8, "X")
    assert sorted(board.available_moves()) == [1, 2, 3, 5, 6, 7]


def test_available_moves_empty_when_board_full():
    """A full board should have no available moves left."""
    board = Board()
    _place_marks(board, [
        (0, "X"), (1, "O"), (2, "X"),
        (3, "X"), (4, "O"), (5, "O"),
        (6, "O"), (7, "X"), (8, "X"),
    ])
    assert board.available_moves() == []


# -------------------------------------------------------------------------
# Reset
# -------------------------------------------------------------------------

def test_reset_clears_the_board():
    """Reset should return the board to a fresh empty state."""
    board = Board()
    _place_marks(board, [(0, "X"), (4, "O"), (8, "X")])
    board.reset()
    assert board.cells == [" "] * 9
    assert board.winner() is None
    assert not board.is_game_over()
    assert sorted(board.available_moves()) == list(range(9))
