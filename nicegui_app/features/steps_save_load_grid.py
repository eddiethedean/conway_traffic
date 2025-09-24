from behave import given, when, then
from nicegui_app.grid_persistence import Grid
import os

@given('the grid is initialized with width {width:d} and height {height:d}')
def step_impl(context, width, height):
    context.grid = Grid(width, height)

@when('the user toggles cell ({x:d}, {y:d}) to blue')
def step_impl(context, x, y):
    context.grid.cells[y][x].is_blue = True

@when('the user saves the grid')
def step_impl(context):
    context.save_path = 'test_saved_grid.json'
    context.grid.save_to_file(context.save_path)

@when('the user clears all cells')
def step_impl(context):
    for row in context.grid.cells:
        for cell in row:
            cell.is_blue = False

@when('the user loads the grid')
def step_impl(context):
    context.grid = Grid.load_from_file(context.save_path)

@then('cell ({x:d}, {y:d}) should be blue')
def step_impl(context, x, y):
    assert context.grid.cells[y][x].is_blue

@then('all other cells should be black')
def step_impl(context):
    for y, row in enumerate(context.grid.cells):
        for x, cell in enumerate(row):
            if not (x == 2 and y == 2):
                assert not cell.is_blue

# Clean up after tests
def after_scenario(context, scenario):
    if hasattr(context, 'save_path') and os.path.exists(context.save_path):
        os.remove(context.save_path)
