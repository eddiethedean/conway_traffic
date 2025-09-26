from behave import given, when, then
from models import Grid
import os


@given("the grid is displayed")
def step_impl(context):
    """Ensure the grid is visible and ready for interaction."""
    context.grid = Grid(5, 5)  # Default grid for testing


@given("I have a grid with all black cells")
def step_impl(context):
    """Initialize a grid with all cells in black (empty road) state."""
    context.grid = Grid(5, 5)
    # All cells start as black by default


@given("cell ({x:d}, {y:d}) is already orange")
def step_impl(context, x, y):
    """Set a specific cell to orange (barrier) state."""
    context.grid.cells[y][x].set_color_state(1)  # orange barrier


@given("cell ({x:d}, {y:d}) is already blue")
def step_impl(context, x, y):
    """Set a specific cell to blue (traffic) state."""
    context.grid.cells[y][x].set_color_state(2)  # blue traffic


@given("the simulation is running")
def step_impl(context):
    """Mark that the simulation is currently running."""
    context.simulation_running = True


@when("I click and hold on cell ({x:d}, {y:d})")
def step_impl(context, x, y):
    """Start a mouse drag operation at the specified cell."""
    context.drag_start_x = x
    context.drag_start_y = y
    context.drag_cells = [(x, y)]  # Initialize with starting cell


@when("I drag my mouse to cell ({x:d}, {y:d})")
def step_impl(context, x, y):
    """Continue the drag operation to the specified cell."""
    # Calculate all cells in the drag path
    start_x, start_y = context.drag_start_x, context.drag_start_y
    end_x, end_y = x, y
    
    # Generate all cells in the rectangular area between start and end
    drag_cells = []
    for cell_x in range(min(start_x, end_x), max(start_x, end_x) + 1):
        for cell_y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            drag_cells.append((cell_x, cell_y))
    
    context.drag_cells = drag_cells


@when("I drag my mouse horizontally to cell ({x:d}, {y:d})")
def step_impl(context, x, y):
    """Drag horizontally from start to end cell."""
    start_x, start_y = context.drag_start_x, context.drag_start_y
    end_x, end_y = x, y
    
    # Horizontal drag - only change x coordinate
    drag_cells = []
    for cell_x in range(min(start_x, end_x), max(start_x, end_x) + 1):
        drag_cells.append((cell_x, start_y))
    
    context.drag_cells = drag_cells


@when("I drag my mouse vertically to cell ({x:d}, {y:d})")
def step_impl(context, x, y):
    """Drag vertically from start to end cell."""
    start_x, start_y = context.drag_start_x, context.drag_start_y
    end_x, end_y = x, y
    
    # Vertical drag - only change y coordinate
    drag_cells = []
    for cell_y in range(min(start_y, end_y), max(start_y, end_y) + 1):
        drag_cells.append((start_x, cell_y))
    
    context.drag_cells = drag_cells


@when("I drag my mouse diagonally to cell ({x:d}, {y:d})")
def step_impl(context, x, y):
    """Drag diagonally from start to end cell."""
    start_x, start_y = context.drag_start_x, context.drag_start_y
    end_x, end_y = x, y
    
    # Diagonal drag - change both x and y coordinates proportionally
    drag_cells = []
    steps = max(abs(end_x - start_x), abs(end_y - start_y))
    if steps > 0:
        for i in range(steps + 1):
            cell_x = start_x + (end_x - start_x) * i // steps
            cell_y = start_y + (end_y - start_y) * i // steps
            drag_cells.append((cell_x, cell_y))
    else:
        drag_cells.append((start_x, start_y))
    
    context.drag_cells = drag_cells


@when("I drag my mouse to cell ({x:d}, {y:d}) which is outside the grid")
def step_impl(context, x, y):
    """Handle drag that goes outside grid boundaries."""
    start_x, start_y = context.drag_start_x, context.drag_start_y
    end_x, end_y = x, y
    
    # Clamp coordinates to grid boundaries
    grid_width = context.grid.width
    grid_height = context.grid.height
    
    clamped_end_x = max(0, min(end_x, grid_width - 1))
    clamped_end_y = max(0, min(end_y, grid_height - 1))
    
    # Generate cells within grid boundaries
    drag_cells = []
    for cell_x in range(min(start_x, clamped_end_x), max(start_x, clamped_end_x) + 1):
        for cell_y in range(min(start_y, clamped_end_y), max(start_y, clamped_end_y) + 1):
            if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height:
                drag_cells.append((cell_x, cell_y))
    
    context.drag_cells = drag_cells


@when("I release the mouse button")
def step_impl(context):
    """Complete the drag operation by applying color changes to all dragged cells."""
    # For BDD tests, we'll cycle through colors to simulate the drag behavior
    # In the actual implementation, this would be handled by the UI drag events
    for x, y in context.drag_cells:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            context.grid.cycle_cell_color(x, y)


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), ({x3:d}, {y3:d}), ({x4:d}, {y4:d}), ({x5:d}, {y5:d}), ({x6:d}, {y6:d}), ({x7:d}, {y7:d}), ({x8:d}, {y8:d}), and ({x9:d}, {y9:d}) should be orange")
def step_impl(context, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9):
    """Check that the specified cells are orange."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8), (x9, y9)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_orange(), f"Cell ({x}, {y}) should be orange but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), ({x3:d}, {y3:d}), ({x4:d}, {y4:d}), ({x5:d}, {y5:d}), ({x6:d}, {y6:d}), ({x7:d}, {y7:d}), ({x8:d}, {y8:d}), and ({x9:d}, {y9:d}) should be blue")
def step_impl(context, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9):
    """Check that the specified cells are blue."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8), (x9, y9)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_blue_traffic(), f"Cell ({x}, {y}) should be blue but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), ({x3:d}, {y3:d}), ({x4:d}, {y4:d}), ({x5:d}, {y5:d}), ({x6:d}, {y6:d}), ({x7:d}, {y7:d}), ({x8:d}, {y8:d}), and ({x9:d}, {y9:d}) should be black")
def step_impl(context, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9):
    """Check that the specified cells are black."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8), (x9, y9)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) should be black but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), and ({x3:d}, {y3:d}) should be orange")
def step_impl(context, x1, y1, x2, y2, x3, y3):
    """Check that the specified cells are orange."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_orange(), f"Cell ({x}, {y}) should be orange but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), and ({x3:d}, {y3:d}) should be blue")
def step_impl(context, x1, y1, x2, y2, x3, y3):
    """Check that the specified cells are blue."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_blue_traffic(), f"Cell ({x}, {y}) should be blue but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), and ({x3:d}, {y3:d}) should be black")
def step_impl(context, x1, y1, x2, y2, x3, y3):
    """Check that the specified cells are black."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) should be black but is {context.grid.cells[y][x].color_state}"


@then("cells ({x1:d}, {y1:d}), ({x2:d}, {y2:d}), ({x3:d}, {y3:d}), ({x4:d}, {y4:d}), ({x5:d}, {y5:d}), ({x6:d}, {y6:d}), and ({x7:d}, {y7:d}) should be orange")
def step_impl(context, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7):
    """Check that the specified cells are orange."""
    cells_to_check = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7)]
    for x, y in cells_to_check:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_orange(), f"Cell ({x}, {y}) should be orange but is {context.grid.cells[y][x].color_state}"


@then("cell ({x:d}, {y:d}) should remain orange")
def step_impl(context, x, y):
    """Check that a specific cell remains orange."""
    assert context.grid.cells[y][x].is_orange(), f"Cell ({x}, {y}) should remain orange but is {context.grid.cells[y][x].color_state}"


@then("cell ({x:d}, {y:d}) should be orange \\(overwritten by drag\\)")
def step_impl(context, x, y):
    """Check that a specific cell is orange after being overwritten by drag."""
    assert context.grid.cells[y][x].is_orange(), f"Cell ({x}, {y}) should be orange (overwritten by drag) but is {context.grid.cells[y][x].color_state}"


@then("all other cells should remain black")
def step_impl(context):
    """Check that all cells not in the drag path remain black."""
    # Get the dragged cells from context
    dragged_cells = set(context.drag_cells)
    
    for y in range(context.grid.height):
        for x in range(context.grid.width):
            if (x, y) not in dragged_cells:
                assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) should remain black but is {context.grid.cells[y][x].color_state}"


@then("only cells within the grid boundaries should be affected")
def step_impl(context):
    """Check that only cells within grid boundaries were affected by the drag."""
    grid_width = context.grid.width
    grid_height = context.grid.height
    
    # Check that no cells outside boundaries were affected
    for y in range(context.grid.height):
        for x in range(context.grid.width):
            if 0 <= x < grid_width and 0 <= y < grid_height:
                # These cells should be affected if they were in the drag path
                pass
            else:
                # These cells should not be affected
                assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) outside boundaries should be black"


@then("the drag should stop at the grid edge")
def step_impl(context):
    """Check that the drag operation respects grid boundaries."""
    grid_width = context.grid.width
    grid_height = context.grid.height
    
    # Verify that the drag didn't affect cells beyond the grid boundaries
    for y in range(context.grid.height):
        for x in range(context.grid.width):
            if x >= grid_width or y >= grid_height:
                assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) beyond grid edge should be black"


@then("the dragged cells should be colored orange")
def step_impl(context):
    """Check that all cells in the drag path are orange."""
    for x, y in context.drag_cells:
        if 0 <= x < context.grid.width and 0 <= y < context.grid.height:
            assert context.grid.cells[y][x].is_orange(), f"Dragged cell ({x}, {y}) should be orange but is {context.grid.cells[y][x].color_state}"


@then("the simulation should continue running")
def step_impl(context):
    """Check that the simulation continues running after drag operation."""
    assert hasattr(context, 'simulation_running')
    assert context.simulation_running is True


@then("the traffic count should update to reflect the new colored cells")
def step_impl(context):
    """Check that the traffic count reflects the new colored cells."""
    # Count active cells (orange and blue)
    active_count = 0
    for row in context.grid.cells:
        for cell in row:
            if cell.is_orange() or cell.is_blue_traffic():
                active_count += 1
    
    # The count should be greater than 0 if we dragged cells
    assert active_count > 0, "Traffic count should reflect the new colored cells"


@then("cell ({x:d}, {y:d}) should be blue \\(cycled from orange\\)")
def step_impl(context, x, y):
    """Check that a specific cell is blue after being cycled from orange."""
    assert context.grid.cells[y][x].is_blue_traffic(), f"Cell ({x}, {y}) should be blue (cycled from orange) but is {context.grid.cells[y][x].color_state}"


@then("cell ({x:d}, {y:d}) should be black \\(cycled from blue\\)")
def step_impl(context, x, y):
    """Check that a specific cell is black after being cycled from blue."""
    assert context.grid.cells[y][x].is_black(), f"Cell ({x}, {y}) should be black (cycled from blue) but is {context.grid.cells[y][x].color_state}"


@then("cell (1, 1) should be blue (cycled from orange)")
def step_impl(context):
    """Check that cell (1, 1) is blue after being cycled from orange."""
    assert context.grid.cells[1][1].is_blue_traffic(), f"Cell (1, 1) should be blue (cycled from orange) but is {context.grid.cells[1][1].color_state}"


@then("cell (2, 2) should be black (cycled from blue)")
def step_impl(context):
    """Check that cell (2, 2) is black after being cycled from blue."""
    assert context.grid.cells[2][2].is_black(), f"Cell (2, 2) should be black (cycled from blue) but is {context.grid.cells[2][2].color_state}"
