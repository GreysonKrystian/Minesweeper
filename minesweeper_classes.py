from random import randint
from itertools import product
from minesweeper_errors import (
    check_board_coordinates,
    WrongSymbolError,
    InvalidCoordinatesFormatError, check_if_in_range, WrongClassError
)
import time


class Board:
    def __init__(self, rows=2, columns=2):
        self._columns = columns
        self._rows = rows
        check_board_coordinates((rows, columns))
        if type(rows) != int or type(columns) != int:
            raise ValueError("Coordinates of board must be integers.")
        self.visualization = [[]]

    def columns(self):
        """
        Get attribute : columns of the board.
        """
        return self._columns

    def rows(self):
        """
        Get attribute : rows of the board.
        """
        return self._rows

    def set_columns(self, new_columns):
        """
        Setter for attribute of Board : column
        """
        check_board_coordinates((new_columns,))
        self._columns = new_columns

    def set_rows(self, new_rows):
        """
        Setter for attribute of Board : row
        """
        check_board_coordinates((new_rows,))
        self._rows = new_rows

    def get_coordinates_info(self, row_pos, column_pos):
        """
        Returns content of given cell of the board.
        Rows and columns are counted from 1
        (for ex. third column has number 2).
        """
        check_board_coordinates((row_pos, column_pos))
        return self.visualization[row_pos][column_pos]

    def set_coordinates(self, row_pos, column_pos, value):
        """
        Modifies given board cell with given value.
        """
        check_board_coordinates((row_pos, column_pos))
        self.visualization[row_pos][column_pos] = str(value)

    def search_symbol_coordinates(self, symbol):
        """
        Searches board for given symbol. Returns a list of coordinates
        where this symbol appears. Only digits and certain symbols are allowed.
        """
        allowed_symbols = ['?', '.', '*']
        if type(symbol) != str:
            raise TypeError('Symbol must be string type')
        if not symbol.lstrip('-').isdigit() and symbol not in allowed_symbols:
            raise WrongSymbolError(f'Given symbol is not in allowed_symbols: {allowed_symbols}')
        symbol_coordinates = []
        for row_index, each_row in enumerate(self.visualization):
            for column_index, cell in enumerate(each_row):
                if cell == symbol:
                    i_col = each_row.index(cell, column_index)
                    i_row = self.visualization.index(each_row, row_index)
                    symbol_coordinates.append((i_row, i_col))
        return symbol_coordinates

    def set_visualization(self, rows, columns):
        """
        creates empty
        """
        if rows != self.rows() or columns != self.columns():
            raise ValueError
        self.visualization = [["."] * columns for index in range(rows)]

    def fill_mines(self, mines, first_move):
        """
        Places randomly given amount of mines on board.
        Uses random.randint for choosing cell
        in which the bomb will be planted.
        Ignores first chosen by player cell.
        """
        check_board_coordinates(first_move)
        check_if_in_range(first_move[0], first_move[1], self.rows(), self.columns())
        mines_to_plant = mines.amount()
        while mines_to_plant > 0:
            random_row = randint(0, self._rows-1)
            random_column = randint(0, self._columns-1)
            cell = self.get_coordinates_info(random_row, random_column)
            if cell != '*' and (random_row, random_column) != first_move:
                self.set_coordinates(random_row, random_column, "*")
                mines_to_plant -= 1

    def cell_neighbours(self, row, column):
        """
        Returns list of coordinates of all possible neighbors of
        base cell with given row and column.
        """
        check_board_coordinates((row, column))
        check_if_in_range(row, column, self.rows(), self.columns())
        possible_rows = [row, row+1, row-1]
        possible_columns = [column, column+1, column-1]  # determine possible neighbors of cell
        for check_row in possible_rows:
            if check_row < 0 or check_row >= self.rows():
                possible_rows.pop(possible_rows.index(check_row))
        for check_column in possible_columns:
            if check_column < 0 or check_column >= self.columns():
                possible_columns.pop(possible_columns.index(check_column))
        combinations = list(product(possible_rows, possible_columns))
        combinations.pop(0)  # base cell has to be ignored
        return combinations

    def info_about_mines_pos(self):
        """
        Modifies board that it contains numbers which inform
        player about mines adjacent to certain cell of the board.
        Function uses product from itertools module to determine
        surrounding of certain cell.
        """
        mines_coords = self.search_symbol_coordinates('*')
        for coordinates in mines_coords:
            row, column = coordinates
            combinations = self.cell_neighbours(row, column)
            for mine_neighbour in combinations:
                symbol = self.get_coordinates_info(mine_neighbour[0], mine_neighbour[1])
                if not symbol.isdigit() and symbol != "*":
                    symbol = "1"
                elif symbol.isdigit():
                    symbol = int(symbol) + 1
                self.set_coordinates(mine_neighbour[0], mine_neighbour[1], symbol)

    def adjacent_symbols(self, combinations):
        """
        Returns list of all adjacent symbols of board's cell
        """
        neighbour_indexes = []
        for neighbour in combinations:
            if len(neighbour) != 2:
                raise InvalidCoordinatesFormatError()
            neighbour_indexes.append(self.get_coordinates_info(neighbour[0], neighbour[1]))
        return neighbour_indexes


class Entity:
    def __init__(self, amount=0, symbol=None):
        if type(amount) != int:
            raise TypeError('Amount of entity must be natural number')
        if amount < 0:
            raise ValueError('Number of given entity cannot be negative')
        if symbol is not None and type(symbol) is not str:
            raise WrongSymbolError('Symbol of entity must be string type')
        self._symbol = symbol
        self._amount = amount

    def amount(self):
        """
        Getter of number of certain entity in the game
        """
        return self._amount

    def symbol(self):
        """
        Get symbol of certain entity
        """
        return self._symbol


class Mines(Entity):
    def __init__(self, mines=0, symbol="*"):
        super().__init__(mines, symbol)

    def set_mines(self, amount_of_mines):
        """
        set amount of mines to given positive number
        """
        if amount_of_mines < 1:
            raise ValueError('There must be at least one mine!')
        self._amount = amount_of_mines

    def coordinate_list(self, board):
        """
        returns list of coordinates of board which contain mines
        """
        return board.search_symbol_coordinates("*")


class Flag(Entity):
    def __init__(self, flags_placed=0, symbol="?"):
        super().__init__(flags_placed, symbol)
        self._flag_coordinates = []

    def flag_coordinates(self):
        """
        Getter of list of coordinates with placed flags
        """
        return self._flag_coordinates

    def add_flag(self, row, column):
        check_board_coordinates((row, column))
        if (row, column) not in self._flag_coordinates:
            self._flag_coordinates.append((row, column))

    def remove_flag(self, row, column):
        check_board_coordinates((row, column))
        if (row, column) in self._flag_coordinates:
            self._flag_coordinates.pop(self._flag_coordinates.index((row, column)))


class Island(Entity):
    def __init__(self, island_board, amount=0, icon='.'):
        super().__init__(amount, icon)
        self._island_board = island_board

    def island_board(self):
        """
        Stores information about position
        of each island. When player reveal one part of island, then
        it will reveal entire island.
        """
        return self._island_board

    def map_islands(self, board):
        """
        fills island board with indexes of islands.
        """
        if not isinstance(board, Board):
            raise WrongClassError("You must give object of Board class as argument")
        island_index = 0
        island_parts_coordinates = board.search_symbol_coordinates('.')
        for row, column in island_parts_coordinates:
            neighbour_digits = []
            neighbors = self._island_board.cell_neighbours(row, column)
            for cell_row, cell_column in neighbors:
                cell_icon = self._island_board.get_coordinates_info(cell_row, cell_column)
                if cell_icon.isdigit():
                    neighbour_digits.append(cell_icon)
            if neighbour_digits:
                self._island_board.set_coordinates(row, column, min(neighbour_digits))
            else:
                island_index += 1
                self._island_board.set_coordinates(row, column, island_index)
        for island_number in range(1, island_index):  # combines islands connected with each other on island board
            island_coords = self._island_board.search_symbol_coordinates(str(island_number))
            for row, column in island_coords:
                neighbours = self._island_board.cell_neighbours(row, column)
                for neighbour_row, neighbour_column in neighbours:
                    connected_island = self._island_board.get_coordinates_info(neighbour_row, neighbour_column)
                    if connected_island.isdigit() and int(connected_island) != island_number:
                        merge_coordinates = self._island_board.search_symbol_coordinates(connected_island)
                        for merge_row, merge_column in merge_coordinates:
                            self._island_board.set_coordinates(merge_row, merge_column, str(island_number))

    def calculate_islands(self):
        """
        calculates number of total islands
        returns list of island indexes
        """
        island_numbers = []
        for row in self._island_board.visualization:
            for island_part in row:
                if island_part.isdigit() and island_part not in island_numbers:
                    island_numbers.append(island_part)
        self._amount = len(island_numbers)
        return island_numbers


class Difficulty:
    def __init__(self, name, board_size, number_of_mines):
        self.name = str(name)
        self.board_size = board_size
        check_board_coordinates(board_size)
        self.number_of_mines = number_of_mines
        if number_of_mines < 0:
            raise ValueError

    def __str__(self):
        mines = self.number_of_mines
        name = self.name
        (row, column) = self.board_size
        s, form = ('', 'is') if mines == 1 else ('s', 'are')
        return f'You have chosen {name.lower()} difficulty.\n\
Size of board is {row}x{column}.\n\
Be careful, there {form} {mines} mine{s}.'

    def insert_difficulty(self, play_board, island_board, mines):
        """
        Changes difficulty by changing board size,
        also changes number of mines.
        """
        if not isinstance(play_board, Board) or not isinstance(island_board, Board) or not isinstance(mines, Mines):
            raise WrongClassError("Wrong object used")
        (new_row, new_column) = self.board_size
        play_board.set_rows(new_row)
        play_board.set_columns(new_column)
        island_board.set_rows(new_row)
        island_board.set_columns(new_column)
        mines.set_mines(self.number_of_mines)


class Game:
    def __init__(self, play_board, flags, islands, mines):
        if not isinstance(play_board, Board) or not isinstance(flags, Flag):
            raise WrongClassError()
        if not isinstance(islands, Island) or not isinstance(mines, Mines):
            raise WrongClassError()
        self.play_board = play_board
        self.flags = flags
        self.islands = islands
        self.mines = mines
        self._number_of_moves = 0
        self._remaining_tiles = []
        self.time = 0

    def number_of_moves(self):
        """
        Get number of moves player made during game.
        """
        return self._number_of_moves

    def made_move(self):
        """
        Increment number of moves.
        """
        self._number_of_moves += 1

    def remaining_tiles(self):
        """
        Get list of coordinates not revealed by player.
        """
        return self._remaining_tiles

    def index_tiles(self):
        """
        Creates collection of all coordinates of the game's board
        """
        for row in range(0, self.play_board.rows()):
            for column in range(0, self.play_board.columns()):
                self._remaining_tiles.append((row, column))

    def winning_conditions(self):
        """
        Checks if condition of win are met.
        """
        mines_coordinates = self.mines.coordinate_list(self.play_board)
        flags_coordinates = self.flags.flag_coordinates()
        flags_win = (sorted(flags_coordinates) == sorted(mines_coordinates))
        cleared_board_win = (sorted(mines_coordinates) == sorted(self._remaining_tiles))
        if cleared_board_win or flags_win:
            return True
        else:
            return False

    def toogle_time(self):
        """
        Returns current time
        """
        return time.time()

    def calculate_3bv(self):
        """
        calculates 3bv indicator
        return value of this indicator.
        """
        bv = 0
        self.islands.calculate_islands()
        for row_index, rows in enumerate(self.play_board.visualization):
            for column_index, tile_symbol in enumerate(rows):
                if tile_symbol.isdigit():
                    island_cell_neighbours = self.islands.island_board().cell_neighbours(row_index, column_index)
                    island_cell_neighbours_icons = self.islands.island_board().adjacent_symbols(island_cell_neighbours)
                    if not any(cell.isdigit() for cell in island_cell_neighbours_icons):
                        bv += 1
        bv += self.islands.amount()
        return bv
