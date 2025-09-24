import pytest
from models import Cell


class TestCell:
    def test_cell_initialization(self):
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert cell.is_blue == False

    def test_cell_initialization_with_color(self):
        cell = Cell(3, 7, is_blue=True)
        assert cell.x == 3
        assert cell.y == 7
        assert cell.is_blue == True

    def test_cell_toggle(self):
        cell = Cell(1, 2)
        assert cell.is_blue == False

        cell.toggle()
        assert cell.is_blue == True

        cell.toggle()
        assert cell.is_blue == False

    def test_multiple_toggles(self):
        cell = Cell(0, 0)
        for i in range(1, 11):
            cell.toggle()
            expected_blue = i % 2 == 1
            assert cell.is_blue == expected_blue
