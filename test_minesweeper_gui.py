import pytest
from PySide2.QtCore import Qt

from minesweeper_classes import Game, Flag, Island, Board, Mines
from minesweeper_errors import IconNotInKeysError
from minesweeper_gui import icon_path, SetDifficulty, MinesweeperBoard


def test_icon_paths():
    icon = icon_path('number_icon', 5)
    assert  icon == 'Minesweeper_Icon_5.png'


def test_icon_wrong_path():
    with pytest.raises(IconNotInKeysError):
        icon_path('Bombs')


def test_create_board(qtbot):
    game1 = Game(Board(3, 5), Flag(), Island(Board(3, 5)), Mines())
    board_gui = MinesweeperBoard(game1)
    board_gui.configure_table()
    assert board_gui.table.rowCount() == 3
    assert board_gui.table.columnCount() == 5
    assert board_gui.moves_label.text() == 'Current move:'
    assert board_gui.flags_label.text() == 'Flags placed:'


def test_set_difficulty(qtbot):
    game1 = Game(Board(), Flag(), Island(Board()), Mines())
    difficulty_gui = SetDifficulty(MinesweeperBoard(game1), game1)
    confirm_button = difficulty_gui.difficulty_ui.confirmButton
    qtbot.addWidget(difficulty_gui)
    assert difficulty_gui.difficulty_ui.startButton.isEnabled() is False
    qtbot.mouseClick(confirm_button, Qt.LeftButton)
    assert difficulty_gui.difficulty_ui.startButton.isEnabled() is True
    assert difficulty_gui.difficulty_ui.infoLabel.text() == 'You have chosen easy difficulty.\n' \
                                                            'Size of board is 9x9.\n' \
                                                            'Be careful, there are 10 mines.'


def test_set_custom_difficulty(qtbot):
    game1 = Game(Board(), Flag(), Island(Board()), Mines())
    difficulty_gui = SetDifficulty(MinesweeperBoard(game1), game1)
    qtbot.addWidget(difficulty_gui)
    assert difficulty_gui.difficulty_ui.customBox.isChecked() is False
    difficulty_gui.difficulty_ui.customBox.setChecked(True)
    assert difficulty_gui.difficulty_ui.columnsSlider.isEnabled() is True
    assert difficulty_gui.difficulty_ui.rowsSlider.isEnabled() is True
    assert difficulty_gui.difficulty_ui.minesSlider.isEnabled() is True
    confirm_button = difficulty_gui.difficulty_ui.confirmButton
    qtbot.mouseClick(confirm_button, Qt.LeftButton)
    assert difficulty_gui.difficulty_ui.infoLabel.text() == 'You have chosen custom difficulty.\n' \
                                                            'Size of board is 2x2.\n' \
                                                            'Be careful, there are 2 mines.'


def test_wrong_difficulty(qtbot):
    game1 = Game(Board(), Flag(), Island(Board()), Mines())
    difficulty_gui = SetDifficulty(MinesweeperBoard(game1), game1)
    qtbot.addWidget(difficulty_gui)
    difficulty_gui.difficulty_ui.customBox.setChecked(True)
    assert difficulty_gui.difficulty_ui.customBox.isChecked() is True
    difficulty_gui.difficulty_ui.columnsSlider.setValue(3)
    difficulty_gui.difficulty_ui.rowsSlider.setValue(10)
    difficulty_gui.difficulty_ui.minesSlider.setValue(100)
    confirm_button = difficulty_gui.difficulty_ui.confirmButton
    assert difficulty_gui.difficulty_ui.startButton.isEnabled() is False
    qtbot.mouseClick(confirm_button, Qt.LeftButton)
    assert difficulty_gui.difficulty_ui.startButton.isEnabled() is False

