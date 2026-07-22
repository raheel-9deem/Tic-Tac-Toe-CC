# Tic Tac Toe

A terminal-based two-player Tic Tac Toe game written in Python. Two players
share the keyboard and take turns placing `X` and `O` on a 3x3 grid. No AI
opponent — just two humans, a terminal, and a scoreboard tracking the session.

## Requirements

- Python 3.8 or later
- No third-party runtime dependencies

## Installation

Clone or download this repository, then open a terminal in the project
directory. There is nothing to install to play the game.

To run the test suite you will need [pytest](https://pytest.org/):

```bash
pip install pytest
```

## How to play

Run the game from the project directory:

```bash
python tic_tac_toe.py
```

1. Enter a name for each player. The first name entered plays as `X` and goes
   first; the second plays as `O`.
2. On your turn, enter a number from **1 to 9** to place your mark in that cell.
   Cells are numbered row by row:

   ```
    1 | 2 | 3
    ----------
    4 | 5 | 6
    ----------
    7 | 8 | 9
   ```

3. The first player to line up three of their marks in a row, column, or
   diagonal wins. If the board fills with no winner, the game is a draw.
4. After each game the scoreboard is shown. Answer `y` to play another round
   with the same players and running scores, or `n` to quit.
5. Type `q` at any move prompt to quit immediately.

Input is validated: non-numbers, numbers off the board, and already-taken cells
are all rejected with a clear error message, and your turn is not lost.

## Project structure

```
.
├── board.py            # Board class: 9-cell state, rules, win/draw detection
├── tic_tac_toe.py      # Entry point: turns, input, flow control, scoreboard
├── tests/
│   └── test_board.py   # pytest suite for the Board class
├── .github/
│   └── workflows/
│       └── tests.yml   # GitHub Actions CI running pytest on push/PR to main
├── .gitignore          # Python gitignore rules
└── README.md           # This file
```

- **`board.py`** owns the game rules. It exposes a small public API — create a
  `Board`, apply moves with `make_move()`, query `winner()` / `is_full()` /
  `is_game_over()`, and call `reset()` to reuse it for a new round.
- **`tic_tac_toe.py`** is the entry point. It handles player names, turn
  alternation, input validation, and the `Scoreboard` that tracks wins and draws
  across a session.

## Running the tests

From the project root:

```bash
pytest tests/
```

Or for verbose output showing each test:

```bash
pytest tests/ -v
```

The test suite covers win detection for every row, column, and diagonal; draw
detection; invalid move handling (out-of-range, occupied, overwriting); and
`available_moves()` correctness.

Tests also run automatically on every push and pull request to `main` via the
GitHub Actions workflow in `.github/workflows/tests.yml`.
