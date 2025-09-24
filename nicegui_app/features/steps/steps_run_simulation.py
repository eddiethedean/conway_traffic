from behave import given, when, then
from models import Grid
from simulation import run_conway_step
import os


@given("the grid is initialized with width {width:d} and height {height:d}")
def step_impl(context, width, height):
    context.grid = Grid(width, height)


@given("the app is running")
def step_impl(context):
    context.grid = Grid(5, 5)  # Default grid for app scenarios


@when("the user toggles cell ({x:d}, {y:d}) to blue")
def step_impl(context, x, y):
    # Set cell to blue traffic state (color_state = 2)
    context.grid.cells[y][x].set_color_state(2)


@given("the user toggles cell ({x:d}, {y:d}) to blue")
def step_impl(context, x, y):
    # Set cell to blue traffic state (color_state = 2)
    context.grid.cells[y][x].set_color_state(2)


@when("the user toggles cell ({x:d}, {y:d}) to orange")
def step_impl(context, x, y):
    context.grid.cells[y][x].set_color_state(1)  # orange barrier


@when("the user clicks the Run button")
def step_impl(context):
    context.grid = run_conway_step(context.grid)


@when("the user saves the grid")
def step_impl(context):
    context.save_path = "test_saved_grid.json"
    context.grid.save_to_file(context.save_path)


@when("the user clears all cells")
def step_impl(context):
    context.grid.clear_all()


@when("the user loads the grid")
def step_impl(context):
    context.grid = Grid.load_from_file(context.save_path)


@then("cell ({x:d}, {y:d}) should be blue")
def step_impl(context, x, y):
    assert context.grid.cells[y][x].is_blue_traffic()


@then("cell ({x:d}, {y:d}) should be orange")
def step_impl(context, x, y):
    assert context.grid.cells[y][x].is_orange()


@then("cell ({x:d}, {y:d}) should be black")
def step_impl(context, x, y):
    assert context.grid.cells[y][x].is_black()


@then("all other cells should be black")
def step_impl(context):
    for y, row in enumerate(context.grid.cells):
        for x, cell in enumerate(row):
            if not ((x == 2 and y == 1) or (x == 2 and y == 2) or (x == 2 and y == 3)):
                assert cell.is_black()


@then("all cells should be black")
def step_impl(context):
    for row in context.grid.cells:
        for cell in row:
            assert cell.is_black()


@given("I set some cells to orange and blue")
def step_impl(context):
    # Set up some test cells
    context.grid.cells[1][1].set_color_state(1)  # orange
    context.grid.cells[2][2].set_color_state(2)  # blue
    context.grid.cells[3][3].set_color_state(1)  # orange


@when('I click the "Save Pattern" button')
def step_impl(context):
    context.save_path = "test_saved_grid.json"
    context.grid.save_to_file(context.save_path)


@when('I click the "Clear All" button')
def step_impl(context):
    context.grid.clear_all()


@when('I click the "Load Pattern" button')
def step_impl(context):
    context.grid = Grid.load_from_file(context.save_path)


@then("the previously set orange and blue cells should be restored")
def step_impl(context):
    # Check that the saved cells are restored
    assert context.grid.cells[1][1].is_orange()
    assert context.grid.cells[2][2].is_blue_traffic()
    assert context.grid.cells[3][3].is_orange()


# Clean up after tests
def after_scenario(context, scenario):
    if hasattr(context, "save_path") and os.path.exists(context.save_path):
        os.remove(context.save_path)
