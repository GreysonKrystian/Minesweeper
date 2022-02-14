import pytest

from minesweeper_classes import (
    Board,
    Flag,
    Island,
    Mines,
    Difficulty,
    Game)
from minesweeper_errors import (
    WrongSymbolError,
    WrongCoordinatesTypeError,
    NegativeCoordinatesError, NotInRangeError, InvalidCoordinatesFormatError, WrongClassError
)


def test_wrong_row():
    with pytest.raises(NegativeCoordinatesError):
        Board1 = Board(-1, 2)


def test_wrong_column():
    with pytest.raises(NegativeCoordinatesError):
        Board2 = Board(1, -2)


def test_coordinates_not_int():
    with pytest.raises(TypeError):
        Board3 = Board(1.5, "4.2")


def test_search_symbol():
    Board1 = Board(3, 3)
    with pytest.raises(WrongSymbolError):
        Board1.search_symbol_coordinates("X")


def test_set_negative_visualization():
    Board1 = Board(2, 2)
    with pytest.raises(ValueError):
        Board1.set_visualization(1, 3)


def invalid_first_move():
    Board1 = Board(2, 5)
    with pytest.raises(WrongCoordinatesTypeError):
        Board1.fill_mines(Mines(), (1.4, 2))


def first_move_out_of_range():
    board = Board(3, 3)
    with pytest.raises(NotInRangeError):
        board.fill_mines(Mines(), (6, 4))


def test_adjacent_symbols_wrong_coordinates():
    board = Board(4, 4)
    with pytest.raises(InvalidCoordinatesFormatError):
        board.adjacent_symbols([(3, 3, 3), (2, 1, 5)])


def test_wrong_entity_amount():
    with pytest.raises(TypeError):
        Flag(1.5)


def test_negative_entity_value():
    with pytest.raises(ValueError):
        Mines(-5)


def test_map_islands_wrong_board():
    islands = Island(Board())
    with pytest.raises(WrongClassError):
        islands.map_islands(Mines())


def test_game_wrong_classes():
    with pytest.raises(WrongClassError):
        Game(Board(), Mines(), Flag(), Mines())


def test_setting_difficulty_wrong():
    with pytest.raises(ValueError):
        Difficulty("Difficulty", (4, 4), -3)


def test_insert_difficulty_wrong_class():
    easy = Difficulty("Easy", (8, 8), 10)
    with pytest.raises(WrongClassError):
        easy.insert_difficulty(Flag(), Mines(), Flag())
