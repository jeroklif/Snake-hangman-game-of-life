import os
from pathlib import Path
import pytest
from Project import run_hangman, run_tic_tac_toe, run_game_of_life, Button


# ---------- Fixtures ----------
@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    if os.path.exists("Assets/scores.json"):
        os.remove("Assets/scores.json")


# ---------- Hangman Tests ----------
def test_load_words() -> None:
    """Test word loading from file"""
    path = Path(__file__).parent.parent / "Assets" / "hangman_data.txt"
    words = run_hangman.load_words(str(path))
    assert isinstance(words, list), "Should return a list of words"
    assert len(words) > 0, "List should not be empty"


def test_load_words_file_not_found() -> None:
    """Test default words when file is missing"""
    words = run_hangman.load_words("non_existent_file.txt")
    assert words == ["PYTHON", "HANGMAN", "COMPUTER"], "Should return default words"


def test_hangman_display() -> None:
    """Test word display formatting"""
    display = run_hangman.get_display_word("PYTHON", ["P", "Y"])
    assert display == "P Y _ _ _ _", "Should reveal guessed letters"


# ---------- Game of Life Tests ----------
def test_game_of_life_update() -> None:
    """Test grid update rules"""
    initial_grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    updated_grid = run_game_of_life.update_grid(initial_grid)
    assert isinstance(updated_grid, list), "Should return a 2D grid"


# ---------- Tic-Tac-Toe Tests ----------
def test_tic_tac_toe_winner() -> None:
    """Test win condition detection"""
    test_board = [["X", "X", "X"], [None, None, None], [None, None, None]]
    winner = run_tic_tac_toe.check_winner(test_board)
    assert winner == "X", "Should detect row win"


# ---------- Button Test ----------
def test_button_click() -> None:
    """Test click detection"""
    button = Button(100, 100, 200, 50, (255, 0, 0), "Test")
    assert button.is_clicked((150, 125)), "Should detect click within bounds"
    assert not button.is_clicked((300, 300)), "Should reject out-of-bounds clicks"
