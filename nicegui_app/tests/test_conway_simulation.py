import pytest
from grid_persistence import Grid

def run_conway_step(grid: Grid) -> Grid:
    width, height = grid.width, grid.height
    new_grid = Grid(width, height)
    for y in range(height):
        for x in range(width):
            live_neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid.cells[ny][nx].is_blue:
                            live_neighbors += 1
            if grid.cells[y][x].is_blue:
                new_grid.cells[y][x].is_blue = live_neighbors in [2, 3]
            else:
                new_grid.cells[y][x].is_blue = live_neighbors == 3
    return new_grid

def test_blinker_oscillator():
    grid = Grid(5, 5)
    grid.cells[2][1].is_blue = True
    grid.cells[2][2].is_blue = True
    grid.cells[2][3].is_blue = True

    # First step
    grid = run_conway_step(grid)
    assert grid.cells[1][2].is_blue
    assert grid.cells[2][2].is_blue
    assert grid.cells[3][2].is_blue
    for y in range(5):
        for x in range(5):
            if (x, y) not in [(2, 1), (2, 2), (2, 3)]:
                assert not grid.cells[y][x].is_blue

    # Second step (should return to original)
    grid = run_conway_step(grid)
    assert grid.cells[2][1].is_blue
    assert grid.cells[2][2].is_blue
    assert grid.cells[2][3].is_blue
    for y in range(5):
        for x in range(5):
            if (x, y) not in [(1, 2), (2, 2), (3, 2)]:
                assert not grid.cells[y][x].is_blue

def test_block_still_life():
    grid = Grid(4, 4)
    grid.cells[1][1].is_blue = True
    grid.cells[1][2].is_blue = True
    grid.cells[2][1].is_blue = True
    grid.cells[2][2].is_blue = True

    grid2 = run_conway_step(grid)
    for y in range(4):
        for x in range(4):
            assert grid.cells[y][x].is_blue == grid2.cells[y][x].is_blue

def test_lonely_cell_dies():
    grid = Grid(3, 3)
    grid.cells[1][1].is_blue = True
    grid2 = run_conway_step(grid)
    for y in range(3):
        for x in range(3):
            assert not grid2.cells[y][x].is_blue
