import os
import pytest
from models import Grid


def test_save_and_load_grid(tmp_path):
    # Create a grid and toggle a cell
    grid = Grid(5, 5)
    grid.cells[2][2].is_blue = True
    save_path = tmp_path / "test_grid.json"
    grid.save_to_file(save_path)

    # Clear the grid
    for row in grid.cells:
        for cell in row:
            cell.is_blue = False

    # Load the grid
    loaded_grid = Grid.load_from_file(save_path)

    # Check that (2,2) is blue and all others are black
    for y, row in enumerate(loaded_grid.cells):
        for x, cell in enumerate(row):
            if x == 2 and y == 2:
                assert cell.is_blue
            else:
                assert not cell.is_blue
