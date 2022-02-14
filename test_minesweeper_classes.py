from minesweeper_classes import (
    Board,
    Flag,
    Island,
    Mines,
    Difficulty,
    Game)


def test_created_board():
    board1 = Board(3, 2)
    board1.set_visualization(3, 2)
    assert board1.columns() == 2
    assert len(board1.visualization) == board1.rows()
    assert len(board1.visualization[1]) == board1.columns()


def test_get_coordinates():
    board1 = Board(3, 3)
    board1.set_visualization(3, 3)
    board1.visualization = [
        ["1", '*', "1"],
        ["1", "1", "1"],
        [".", ".", "."]
        ]
    assert board1.get_coordinates_info(0, 1) == '*'


def test_plant_mines():
    board1 = Board(4, 5)
    board1.set_visualization(4,5)
    mine_field = Mines()
    assert mine_field.amount() == 0
    mine_field.set_mines(10)
    assert mine_field.amount() == 10
    board1.fill_mines(mine_field, (3, 3))
    planted_mines = 0
    for each_row in board1.visualization:
        planted_mines += each_row.count('*')
    assert planted_mines == 10


def test_fill_info_about_mines():
    board1 = Board(5, 5)
    board1.set_visualization(5, 5)
    board1.visualization = [
        [".", '*', ".", ".", "."],
        ["*", ".", "*", ".", "."],
        [".", ".", ".", ".", "."],
        [".", "*", ".", ".", "*"],
        [".", ".", "*", ".", "*"]]
    board1.info_about_mines_pos()
    assert board1.visualization == [
            ["2", '*', "2", "1", "."],
            ["*", "3", "*", "1", "."],
            ["2", "3", "2", "2", "1"],
            ["1", "*", "2", "3", "*"],
            ["1", "2", "*", "3", "*"]]


def test_place_and_remove_flag():
    board1 = Board(5, 5)
    flags = Flag()
    assert flags.flag_coordinates() == []
    flags.add_flag(2, 2)
    flags.add_flag(3, 1)
    assert flags.flag_coordinates() == [(2, 2), (3, 1)]
    flags.remove_flag(2, 2)
    assert flags.flag_coordinates() == [(3, 1)]


def test_cell_neighbours_middle():
    board = Board(3, 3)
    assert board.cell_neighbours(1, 1) == [(1, 2), (1, 0), (2, 1), (2, 2), (2, 0), (0, 1), (0, 2), (0, 0)]


def test_cell_neighbours_edge():
    board = Board(3, 3)
    assert board.cell_neighbours(0, 0) == [(0, 1), (1, 0), (1, 1)]


def test_difficulty():
    board1 = Board(5, 5)
    flags = Flag()
    mines = Mines()
    islands = Island(board1)
    assert board1.columns() == 5
    assert board1.rows() == 5
    mines = Mines(2)
    assert mines.amount() == 2
    easy = Difficulty("Easy", (8, 8), 10)
    easy.insert_difficulty(board1, islands.island_board(), mines)
    assert mines.amount() == 10
    assert board1.columns() == 8
    assert board1.rows() == 8
    assert islands.island_board().rows() == 8


def test_str_difficulty():
    easy = Difficulty("Easy", (8, 8), 10)
    str(easy) == 'You have chosen easy difficulty. Size of board if 8x8.\
     Be careful, there are 10 mines. '


def test_island_board():
    board1 = Board(8, 8)
    board1.set_visualization(8, 8)
    board_islands = Board(8, 8)
    board_islands.set_visualization(8, 8)
    islands = Island(board_islands)
    board1.visualization = [
                            ['1', '1', '1', '.', '.', '.', '.', '.'],
                            ['1', '*', '1', '.', '.', '.', '.', '.'],
                            ['2', '2', '1', '.', '.', '1', '1', '1'],
                            ['*', '3', '1', '1', '1', '3', '*', '2'],
                            ['*', '4', '*', '1', '1', '*', '*', '2'],
                            ['2', '*', '2', '1', '1', '3', '4', '3'],
                            ['1', '1', '1', '.', '.', '1', '*', '*'],
                            ['.', '.', '.', '.', '.', '1', '2', '2']]
    islands.map_islands(board1)
    assert board_islands.visualization == [
                            ['.', '.', '.', '1', '1', '1', '1', '1'],
                            ['.', '.', '.', '1', '1', '1', '1', '1'],
                            ['.', '.', '.', '1', '1', '.', '.', '.'],
                            ['.', '.', '.', '.', '.', '.', '.', '.'],
                            ['.', '.', '.', '.', '.', '.', '.', '.'],
                            ['.', '.', '.', '.', '.', '.', '.', '.'],
                            ['.', '.', '.', '2', '2', '.', '.', '.'],
                            ['2', '2', '2', '2', '2', '.', '.', '.']]


def test_no_islands():
    board1 = Board(2, 3)
    board1.set_visualization(2, 3)
    board_island = Board(2, 3)
    board_island.set_visualization(2, 3)
    islands = Island(board_island)
    board1.visualization = [['1', '1', '1'],
                            ['1', '*', '1']]
    islands.map_islands(board1)
    assert board_island.visualization == [['.', '.', '.'],
                                          ['.', '.', '.']]


def test_island_board_2():
    board1 = Board(8, 8)
    board1.set_visualization(8, 8)
    board_islands = Board(8, 8)
    board_islands.set_visualization(8, 8)
    island1 = Island(board_islands)
    board1.visualization = [
       ['*', '*', '2', '1', '2', '*', '*', '3'],
       ['5', '*', '3', '1', '*', '5', '*', '*'],
       ['*', '*', '2', '1', '2', '*', '3', '2'],
       ['3', '3', '1', '.', '1', '2', '2', '1'],
       ['*', '1', '1', '2', '2', '2', '*', '1'],
       ['2', '2', '1', '*', '*', '4', '2', '1'],
       ['*', '2', '1', '4', '*', '*', '1', '.'],
       ['*', '2', '.', '2', '*', '3', '1', '.']]
    island1.map_islands(board1)
    assert island1.island_board().visualization == [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '1', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '2'],
        ['.', '.', '3', '.', '.', '.', '.', '2']]
    island1.calculate_islands()
    assert island1.amount() == 3


def test_island_less_bombs():
    board1 = Board(8, 8)
    board1.set_visualization(8, 8)
    board_islands = Board(8, 8)
    board_islands.set_visualization(8, 8)
    flags = Flag()
    mines = Mines(8)
    islands = Island(board_islands)
    game1 = Game(board1, flags, islands, mines)
    board1.visualization = [['*', '3', '*', '2', '.', '.', '.', '.'],
                            ['1', '3', '*', '2', '.', '.', '.', '.'],
                            ['.', '1', '1', '1', '.', '1', '1', '1'],
                            ['.', '.', '.', '.', '.', '1', '*', '1'],
                            ['.', '.', '.', '.', '.', '1', '1', '1'],
                            ['.', '.', '.', '1', '1', '1', '.', '.'],
                            ['.', '.', '1', '3', '*', '3', '1', '.'],
                            ['.', '.', '1', '*', '*', '*', '1', '.']]

    islands.map_islands(board1)
    assert board_islands.visualization == [
    ['.', '.', '.', '.', '1', '1', '1', '1'],
    ['.', '.', '.', '.', '1', '1', '1', '1'],
    ['1', '.', '.', '.', '1', '.', '.', '.'],
    ['1', '1', '1', '1', '1', '.', '.', '.'],
    ['1', '1', '1', '1', '1', '.', '.', '.'],
    ['1', '1', '1', '.', '.', '.', '3', '3'],
    ['1', '1', '.', '.', '.', '.', '.', '3'],
    ['1', '1', '.', '.', '.', '.', '.', '3']]
    islands.calculate_islands()
    assert islands.amount() == 2
    assert game1.calculate_3bv() == 4


def test_game_winning():
    board1 = Board(2, 2)
    board_islands = Board(2, 2)
    flags = Flag()
    mines = Mines(2)
    islands = Island(board_islands)
    game1 = Game(board1, flags, islands, mines)
    game1.index_tiles()
    assert game1.remaining_tiles() == [(0, 0), (0, 1), (1, 0), (1, 1)]
    board1.visualization = [['*', '1'],
                            ['*', '1']]
    assert game1.winning_conditions() is False
    game1.remaining_tiles().pop(1)
    game1.remaining_tiles().pop(2)
    assert game1.winning_conditions() is True


def test_3bv_calculation():
    board = Board(2, 5)
    board_islands = Board(2, 5)
    board.set_visualization(2, 5)
    board_islands.set_visualization(2, 5)
    flags = Flag()
    mines = Mines(1)
    islands = Island(board_islands)
    board.visualization = [['1', '1', '1', '.', '.'],
                            ['1', '*', '1', '.', '.']]
    islands.map_islands(board)
    game = Game(board, flags, islands, mines)
    islands.calculate_islands()
    assert game.calculate_3bv() == 4
