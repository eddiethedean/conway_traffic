import pytest
from cell import Cell
from grid import Grid
from app import InteractiveGridApp


class TestCell:
    def test_cell_initialization(self):
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert cell.is_blue == False

    def test_cell_toggle(self):
        cell = Cell(1, 2)
        assert cell.is_blue == False
        cell.toggle()
        assert cell.is_blue == True
        cell.toggle()
        assert cell.is_blue == False


class TestGrid:
    def test_grid_initialization(self):
        grid = Grid(5, 3)
        assert grid.width == 5
        assert grid.height == 3
        assert len(grid.cells) == 3
        assert len(grid.cells[0]) == 5

    def test_get_cell(self):
        grid = Grid(3, 3)
        cell = grid.get_cell(1, 1)
        assert cell.x == 1
        assert cell.y == 1

    def test_toggle_cell(self):
        grid = Grid(3, 3)
        grid.toggle_cell(1, 1)
        assert grid.get_cell(1, 1).is_blue == True
        assert grid.get_cell(0, 0).is_blue == False

    def test_resize_grid(self):
        grid = Grid(3, 3)
        grid.toggle_cell(0, 0)
        grid.resize(5, 5)
        assert grid.width == 5
        assert grid.height == 5
        for row in grid.cells:
            for cell in row:
                assert cell.is_blue == False


class TestApp:
    def test_app_initialization(self):
        app = InteractiveGridApp()
        assert app.grid.width == 42
        assert app.grid.height == 25
        assert app.width_input is None
        assert app.height_input is None

    def test_on_cell_click(self):
        app = InteractiveGridApp()
        assert app.grid.get_cell(3, 3).is_blue == False
        app.on_cell_click(3, 3)
        assert app.grid.get_cell(3, 3).is_blue == True

    def test_clear_all(self):
        app = InteractiveGridApp()
        app.grid.toggle_cell(1, 1)
        app.grid.toggle_cell(2, 2)
        assert app.grid.get_cell(1, 1).is_blue == True
        assert app.grid.get_cell(2, 2).is_blue == True

        app.clear_all()
        assert app.grid.get_cell(1, 1).is_blue == False
        assert app.grid.get_cell(2, 2).is_blue == False
