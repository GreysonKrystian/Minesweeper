from minesweeper_errors import check_board_coordinates, IconNotInKeysError
from ui_difficulty import Ui_MainWindow
from PySide2.QtCore import QSize, Qt, QEvent, QObject
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QTableWidget, QLabel
from PySide2.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout
from minesweeper_classes import Board, Flag, Mines, Island, Game, Difficulty
import sys


def icon_path(icon_type, digit=None):
    """
    contains paths of icons used in game. Pictures should be in the same folder as the game.
    """

    icons_path_base = {
        'blank_icon': 'Minesweeper_Empty.png',
        'bomb_icon': 'Minesweeper_Icon_Bomb.png',
        'number_icon': f'Minesweeper_Icon_{digit}.png',
        'flag_icon': 'Minesweeper_Icon_Flag.png'
    }
    if icon_type not in icons_path_base.keys():
        raise IconNotInKeysError("There isn't icon of this name in the database")
    return icons_path_base.get(icon_type, '')


class SetDifficulty(QMainWindow):
    def __init__(self, board_gui, game, parent=None):
        super().__init__(parent)
        self.board_gui = board_gui
        self.Game = game
        self.difficulty_ui = Ui_MainWindow()
        self.difficulty_ui.setupUi(self)
        self.set_level_buttons()
        self.error_popup = QMessageBox()

    def change_custom_state(self, state):
        """
        enables/disables ability to create custom game (QtChecked)
        """
        if state == Qt.Checked:
            self.difficulty_ui.minesSlider.setEnabled(True)
            self.difficulty_ui.rowsSlider.setEnabled(True)
            self.difficulty_ui.columnsSlider.setEnabled(True)

        else:
            self.difficulty_ui.columnsSlider.setEnabled(False)
            self.difficulty_ui.minesSlider.setEnabled(False)
            self.difficulty_ui.rowsSlider.setEnabled(False)
            self.difficulty_ui.rowsSliderLabel.clear()
            self.difficulty_ui.columnsSliderLabel.clear()
            self.difficulty_ui.minesSliderLabel.clear()

    def start_game(self):
        """
        creates board when player presses start game
        """
        self.close()
        self.board_gui.build_game()
        row_screen_size = 26
        column_screen_size = 30
        if self.Game.play_board.rows() < row_screen_size and self.Game.play_board.columns() < column_screen_size:
            self.board_gui.show()
        else:
            self.board_gui.showMaximized()

    def set_level_buttons(self):
        """
        Operates set level button.
        """
        self.difficulty_ui.customBox.stateChanged.connect(self.change_custom_state)
        self.difficulty_ui.columnsSlider.setEnabled(False)
        self.difficulty_ui.minesSlider.setEnabled(False)
        self.difficulty_ui.rowsSlider.setEnabled(False)
        self.difficulty_ui.startButton.setEnabled(False)
        self.difficulty_ui.confirmButton.clicked.connect(self.choose_difficulty)
        self.difficulty_ui.startButton.clicked.connect(self.start_game)
        columns_label = self.difficulty_ui.columnsSliderLabel.setNum
        self.difficulty_ui.columnsSlider.valueChanged.connect(columns_label)
        rows_label = self.difficulty_ui.rowsSliderLabel.setNum
        self.difficulty_ui.rowsSlider.valueChanged.connect(rows_label)
        mines_label = self.difficulty_ui.minesSliderLabel.setNum
        self.difficulty_ui.minesSlider.valueChanged.connect(mines_label)

    def exec_difficulty(self, level):
        """
        inserts chosen difficulty and informs player about that with proper text.
        """
        level.insert_difficulty(self.Game.play_board, self.Game.islands.island_board(), self.Game.mines)
        self.difficulty_ui.infoLabel.setText(str(level))
        self.difficulty_ui.startButton.setEnabled(True)

    def choose_difficulty(self):
        """
        creates customBox of predefined levels which player can choose instead of creating own one.
        """
        premade_levels = {
            "Easy": Difficulty("Easy", (9, 9), 10),
            "Medium": Difficulty("Medium", (13, 15), 40),
            "Hard": Difficulty("Hard", (30, 16), 99)
        }
        if self.difficulty_ui.customBox.checkState():
            rows_amount = self.difficulty_ui.rowsSlider.value()
            columns_amount = self.difficulty_ui.columnsSlider.value()
            mines_amount = self.difficulty_ui.minesSlider.value()
            if mines_amount >= rows_amount*columns_amount:
                self.amount_error_popup()
            else:
                level = Difficulty("Custom", (rows_amount, columns_amount), mines_amount)
                self.exec_difficulty(level)
                self.difficulty_ui.startButton.setEnabled(True)
        else:
            self.difficulty_ui.startButton.setEnabled(True)
            level_chosen = self.difficulty_ui.difficultyBox.currentText()
            level = premade_levels.get(level_chosen)
            self.exec_difficulty(level)

    def amount_error_popup(self):
        """
        error pop-up when player choose more/equal mines to size of board
        """
        self.error_popup = QMessageBox()
        self.error_popup.setWindowTitle("CustomSettingsError")
        self.error_popup.setIcon(QMessageBox.Warning)
        self.error_popup.setText("Number of mines cannot be higher or equal total size of Board!")
        self.error_popup.exec_()


class MinesweeperBoard(QMainWindow):
    def __init__(self, game, parent=None):
        super().__init__(parent)

        self.Game = game
        self.buttons = {}
        self.start_time = 0
        self.table = QTableWidget()
        self.setCentralWidget(self.table)
        self.table_layout = QHBoxLayout(self.centralWidget())
        self.moves_label = QLabel('Current move:')
        self.flags_label = QLabel("Flags placed:")
        self.label_layout = QVBoxLayout()
        self.label_layout.setAlignment(Qt.AlignRight)
        self.label_layout.addWidget(self.flags_label)
        self.label_layout.addWidget(self.moves_label)
        self.table_layout.addLayout(self.label_layout)

    def build_game(self):
        """
        creates board gui with given size.
        """
        self.configure_table()
        rows = self.Game.play_board.rows()
        columns = self.Game.play_board.columns()
        self.Game.play_board.set_visualization(rows, columns)
        self.Game.islands.island_board().set_visualization(rows, columns)
        self.create_buttons()
        self.table.setMaximumSize(self.table_size())
        self.table.setMinimumSize(self.table_size())
        self.Game.index_tiles()

    def table_size(self):
        """
        Scales size of window
        """
        place_for_labels = 130
        board_width = place_for_labels
        for index in range(self.table.columnCount()):
            board_width += self.table.columnWidth(index)
        board_height = 0
        board_height = 30 if self.table.rowCount() < 4 else board_height
        for index in range(self.table.rowCount()):
            board_height += self.table.rowHeight(index)
        return QSize(board_width, board_height)

    def configure_table(self):
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setRowCount(self.Game.play_board.rows())
        self.table.setColumnCount(self.Game.play_board.columns())
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def get_button(self, row, column):
        """
        returns button with given row and column on the board
        """
        check_board_coordinates((row, column))
        return self.buttons.get(f"button{row},{column}")

    def pop_tile(self, row, column):
        """
        removes coordinate of given row and column from remaining tiles when it is clicked.
        """
        check_board_coordinates((row, column))
        if (row, column) in self.Game.remaining_tiles():
            return self.Game.remaining_tiles().pop(self.Game.remaining_tiles().index((row, column)))

    def create_buttons(self):
        """
        Fills table Widget with buttons.
        """
        for row in range(0, self.Game.play_board.rows()):
            screen_size_rows = 20
            screen_size_columns = 30
            if self.Game.play_board.rows() < screen_size_rows and self.Game.play_board.columns() < screen_size_columns:
                self.table.setRowHeight(row, 50)
            else:
                self.table.setRowHeight(row, 30)
            for column in range(0, self.Game.play_board.columns()):
                if self.Game.play_board.rows() < screen_size_rows and self.Game.play_board.columns() < screen_size_columns:
                    self.table.setColumnWidth(column, 50)
                else:
                    self.table.setColumnWidth(column, 30)
                self.buttons[f"button{row},{column}"] = QPushButton("")
                self.table.setCellWidget(row, column, self.get_button(row, column))
                self.get_button(row, column).installEventFilter(self)
                self.get_button(row, column).row = row
                self.get_button(row, column).column = column

    def scale_icons(self, button):
        """
        changes size of icon on the buttons to fit the screen
        """
        if self.Game.play_board.rows() < 20 and self.Game.play_board.columns() < 30:
            button.setIconSize(QSize(45, 45))
        else:
            button.setIconSize(QSize(28, 28))

    def insert_icon(self, button, icon_type, is_digit=None):
        """
        adds icon to button with given type
        """
        path = icon_path(icon_type, is_digit)
        icon = QIcon()
        icon.addPixmap(QPixmap(path), QIcon.Disabled)
        self.scale_icons(button)
        button.setIcon(icon)

    def flag_and_moves_labels_info(self):
        """
        updates labels which shows current move and placed flags to number of mines
        """
        self.moves_label.setText(f'Current move:\n{self.Game.number_of_moves()}')
        self.flags_label.setText(f'Flags placed:\n{len(self.Game.flags.flag_coordinates())}/{self.Game.mines.amount()}')

    def create_mine_field(self, first_click_coordinates):
        row, column = first_click_coordinates
        self.Game.play_board.fill_mines(self.Game.mines, (row, column))
        self.Game.play_board.info_about_mines_pos()
        self.Game.islands.map_islands(self.Game.play_board)
        self.start_time = self.Game.toogle_time()

    def eventFilter(self, button, event):
        """
        recognizes left and right click of a button
        """
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.left_click(button.row, button.column)
            elif event.button() == Qt.RightButton and (button.row, button.column) in self.Game.remaining_tiles():
                self.right_click(button, self.Game.flags.flag_coordinates())
            if self.Game.winning_conditions():
                self.endgame_popup(game_won=True)

        return QObject.event(button, event)

    def right_click(self, button, flag_list):
        """
        handles right click on button
        """
        row = button.row
        column = button.column
        if self.Game.number_of_moves() == 0:
            self.create_mine_field((row, column))
        if (button.row, button.column) in self.Game.remaining_tiles():
            self.Game.made_move()
        if (row, column) not in flag_list:
            button.setEnabled(False)
            self.Game.flags.add_flag(button.row, button.column)
            self.insert_icon(button, 'flag_icon')
        else:
            button.setEnabled(True)
            button.setIcon(QIcon())
            self.Game.flags.remove_flag(button.row, button.column)
        self.flag_and_moves_labels_info()

    def left_click(self, row, column):
        """
        handles left click on button.
        """
        check_board_coordinates((row, column))
        button = self.get_button(row, column)
        if self.Game.number_of_moves() == 0:
            self.create_mine_field((row, column))
        if (button.row, button.column) not in self.Game.flags.flag_coordinates():
            if (button.row, button.column) in self.Game.remaining_tiles():
                self.Game.made_move()
            self.flag_and_moves_labels_info()
            indicator = self.Game.play_board.get_coordinates_info(row, column)
            if indicator == ".":
                empty_icon = QIcon()
                empty_icon.addPixmap(QPixmap(icon_path('blank_icon')), QIcon.Active)
                empty_icon.addPixmap(QPixmap(icon_path('blank_icon')), QIcon.Disabled)
                self.get_button(row, column).setIcon(empty_icon)
                self.scale_icons(button)
                button.setEnabled(False)
                self.pop_tile(row, column)
            if self.Game.winning_conditions():
                self.endgame_popup(game_won=True)
            island_indicator = self.Game.islands.island_board().get_coordinates_info(row, column)
            if indicator == "." and island_indicator.isdigit():
                coordinates = self.Game.islands.island_board().search_symbol_coordinates(island_indicator)
                for row, column in coordinates:
                    if self.get_button(row, column).isEnabled():
                        button = self.get_button(row, column)
                        self.scale_icons(button)
                        button.setIcon(empty_icon)
                        button.setEnabled(False)
                        self.pop_tile(row, column)
                    neighbours_indexes = self.Game.islands.island_board().cell_neighbours(row, column)
                    for neighbour_row, neighbour_column in neighbours_indexes:
                        neighbour_symbol = self.Game.play_board.get_coordinates_info(neighbour_row, neighbour_column)
                        if neighbour_symbol.isdigit():
                            button = self.get_button(neighbour_row, neighbour_column)
                            self.insert_icon(button, 'number_icon', neighbour_symbol)
                            button.setEnabled(False)
                            self.pop_tile(neighbour_row, neighbour_column)
                if self.Game.winning_conditions():
                    self.endgame_popup(game_won=True)
            elif indicator == '*' and self.get_button(row, column).isEnabled():
                bombs = self.Game.play_board.search_symbol_coordinates('*')
                for row, column in bombs:
                    button = self.get_button(row, column)
                    self.insert_icon(button, 'bomb_icon')
                self.endgame_popup(game_won=False)
            elif indicator.isdigit():
                self.insert_icon(button, 'number_icon', indicator)
                self.pop_tile(row, column)

    def endgame_popup(self, game_won):
        """
        shows result of the game after clicking ok program ends
        """
        end_time = self.Game.toogle_time()
        time = end_time - self.start_time
        BV_of_board = self.Game.calculate_3bv()
        popup = QMessageBox()
        popup.setWindowTitle("GAME ENDED")
        if game_won:
            popup.setText("You have won the minesweeper game")
        else:
            popup.setText("You have lost minesweeper game")
        s = "s" if self.Game.number_of_moves() != 1 else ""
        popup.setInformativeText(f"3BV indicator of map you've played is {BV_of_board}.\
            You've made {self.Game.number_of_moves()} move{s} during your game.\
            Time of the game was {time:.2f} seconds")

        popup.setIcon(QMessageBox.Information)
        popup.exec_()
        popup.buttonClicked.connect(sys.exit())
