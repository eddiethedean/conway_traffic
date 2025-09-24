import pytest
from models import Cell, Grid
from app import InteractiveGridApp


class TestCell:
    def test_cell_initialization(self):
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert cell.color_state == 0  # black
        assert not cell.is_blue

    def test_cell_color_cycling(self):
        cell = Cell(1, 2)
        assert cell.color_state == 0  # black
        assert not cell.is_blue

        cell.cycle_color()
        assert cell.color_state == 1  # orange
        assert cell.is_blue  # orange is considered "active"

        cell.cycle_color()
        assert cell.color_state == 2  # blue
        assert cell.is_blue

        cell.cycle_color()
        assert cell.color_state == 0  # back to black
        assert not cell.is_blue


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

    def test_cycle_cell_color(self):
        grid = Grid(3, 3)
        grid.cycle_cell_color(1, 1)
        assert grid.get_cell(1, 1).color_state == 1  # orange
        grid.cycle_cell_color(1, 1)
        assert grid.get_cell(1, 1).color_state == 2  # blue
        assert grid.get_cell(0, 0).color_state == 0  # black

    def test_resize_grid(self):
        grid = Grid(3, 3)
        grid.cycle_cell_color(0, 0)
        grid.resize(5, 5)
        assert grid.width == 5
        assert grid.height == 5
        # Original cell should be preserved
        assert grid.get_cell(0, 0).color_state == 1
        # New cells should be black
        assert grid.get_cell(4, 4).color_state == 0


class TestApp:
    def test_app_initialization(self):
        app = InteractiveGridApp()
        assert app.grid.width == 42
        assert app.grid.height == 25
        assert app.width_input is None
        assert app.height_input is None

    def test_on_cell_click(self):
        app = InteractiveGridApp()
        assert app.grid.get_cell(3, 3).color_state == 0
        app.on_cell_click(3, 3)
        assert app.grid.get_cell(3, 3).color_state == 1  # orange

    def test_clear_all(self):
        app = InteractiveGridApp()
        app.grid.cycle_cell_color(1, 1)
        app.grid.cycle_cell_color(2, 2)
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1

        app.clear_all()
        assert app.grid.get_cell(1, 1).color_state == 0
        assert app.grid.get_cell(2, 2).color_state == 0
