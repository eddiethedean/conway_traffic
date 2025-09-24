from behave import given, when, then
from nicegui_app.grid_persistence import Grid
import os

@given('the grid is initialized with width {width:d} and height {height:d}')
def step_impl(context, width, height):
    context.grid = Grid(width, height)

@when('the user toggles cell ({x:d}, {y:d}) to blue')
def step_impl(context, x, y):
    context.grid.cells[y][x].is_blue = True

@when('the user clicks the Run button')
def step_impl(context):
    context.grid = run_conway_step(context.grid)

@then('cell ({x:d}, {y:d}) should be blue')
def step_impl(context, x, y):
    assert context.grid.cells[y][x].is_blue

@then('all other cells should be black')
def step_impl(context):
    for y, row in enumerate(context.grid.cells):
        for x, cell in enumerate(row):
            if not ((x == 2 and y == 1) or (x == 2 and y == 2) or (x == 2 and y == 3)):
                assert not cell.is_blue

def run_conway_step(grid):
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
