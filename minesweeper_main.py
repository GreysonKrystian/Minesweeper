import sys
from PySide2.QtWidgets import QApplication
from minesweeper_classes import Board, Flag, Mines, Island, Game
from minesweeper_gui import MinesweeperBoard, SetDifficulty


def guiMain(args):
    board1 = Board()
    board_islands = Board()
    flags = Flag()
    mines = Mines()
    islands = Island(board_islands)
    game1 = Game(board1, flags, islands, mines)
    app = QApplication(args)
    board_ui = MinesweeperBoard(game1)
    start_ui = SetDifficulty(board_ui, game1)
    start_ui.show()
    return app.exec_()


if __name__ == "__main__":
    guiMain(sys.argv)
