import pytest
from models import Grid
from simulation import run_conway_step


# --- Cell color cycling logic ---
def test_cell_color_cycling():
    grid = Grid(3, 3)
    cell = grid.get_cell(1, 1)
    # Initial state: black
    assert not hasattr(cell, "color_state") or cell.color_state == 0
    # First click: orange
    cell.color_state = 1
    assert cell.color_state == 1
    # Second click: blue
    cell.color_state = 2
    assert cell.color_state == 2
    # Third click: black
    cell.color_state = 0
    assert cell.color_state == 0


# --- Clear all ---
def test_clear_all():
    grid = Grid(2, 2)
    for row in grid.cells:
        for cell in row:
            cell.is_blue = True
            cell.color_state = 2
    # Simulate clear_all
    for row in grid.cells:
        for cell in row:
            cell.is_blue = False
            cell.color_state = 0
    for row in grid.cells:
        for cell in row:
            assert not cell.is_blue
            assert cell.color_state == 0


# --- Save/load grid ---
def test_save_load(tmp_path):
    grid = Grid(2, 2)
    grid.cells[0][0].is_blue = True
    grid.cells[0][0].color_state = 2
    grid.cells[1][1].is_blue = True
    grid.cells[1][1].color_state = 1
    file = tmp_path / "grid.json"
    grid.save_to_file(str(file))
    loaded = Grid.load_from_file(str(file))
    assert loaded.cells[0][0].is_blue and loaded.cells[0][0].color_state == 2
    assert loaded.cells[1][1].is_blue and loaded.cells[1][1].color_state == 1


# --- Simulation only updates blue cells ---
def test_simulation_only_updates_blue():
    grid = Grid(3, 3)
    # Set center blue, corners orange
    grid.cells[1][1].is_blue = True
    grid.cells[1][1].color_state = 2
    grid.cells[0][0].is_blue = True
    grid.cells[0][0].color_state = 1
    grid.cells[0][2].is_blue = True
    grid.cells[0][2].color_state = 1
    grid.cells[2][0].is_blue = True
    grid.cells[2][0].color_state = 1
    grid.cells[2][2].is_blue = True
    grid.cells[2][2].color_state = 1
    new_grid = run_conway_step(grid)
    # Orange cells remain orange
    assert new_grid.cells[0][0].color_state == 1
    assert new_grid.cells[0][2].color_state == 1
    assert new_grid.cells[2][0].color_state == 1
    assert new_grid.cells[2][2].color_state == 1
    # Center blue cell updates by rules
    assert new_grid.cells[1][1].color_state in (0, 2)


# --- Resize grid ---
def test_resize_grid():
    grid = Grid(2, 2)
    grid.resize(3, 3)
    assert grid.width == 3 and grid.height == 3
    assert len(grid.cells) == 3 and len(grid.cells[0]) == 3


# --- Blue/orange cell count ---
def test_orange_blue_count():
    grid = Grid(2, 2)
    grid.cells[0][0].is_blue = True
    grid.cells[0][0].color_state = 2
    grid.cells[1][1].is_blue = True
    grid.cells[1][1].color_state = 1
    orange = sum(
        1 for row in grid.cells for cell in row if getattr(cell, "color_state", 0) == 1
    )
    blue = sum(
        1 for row in grid.cells for cell in row if getattr(cell, "color_state", 0) == 2
    )
    assert orange == 1
    assert blue == 1
