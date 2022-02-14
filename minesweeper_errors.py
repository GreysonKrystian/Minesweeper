class NegativeCoordinatesError(ValueError):
    pass


class WrongSymbolError(Exception):
    pass


class WrongCoordinatesTypeError(TypeError):
    pass


class InvalidMinesAmountError(TypeError):
    pass


class InvalidCoordinatesFormatError(Exception):
    pass


class IconNotInKeysError(Exception):
    pass


class NotInRangeError(Exception):
    pass

class WrongClassError(Exception):
    pass


def check_board_coordinates(coordinates):
    if type(coordinates) not in (tuple, list):
        raise TypeError("You need tuple or list of coordinates to check if they are correct")
    for coordinate in coordinates:
        if coordinate < 0:
            raise NegativeCoordinatesError("Coordinates of minesweeper board must be greater than zero")


def check_if_in_range(given_row, given_column, number_of_rows, number_of_columns):
    if given_row >= number_of_rows or given_column >= number_of_columns:
        raise NotInRangeError('Given coordinates are out of range.')