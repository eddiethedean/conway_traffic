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

    def test_mouse_drag_initialization(self):
        """Test that mouse drag state is properly initialized."""
        app = InteractiveGridApp()
        assert not app.is_dragging
        assert app.drag_start_x is None
        assert app.drag_start_y is None
        assert app.dragged_cells == []

    def test_mouse_down_starts_drag(self):
        """Test that mouse down starts a drag operation."""
        app = InteractiveGridApp()
        app.on_cell_mouse_down(2, 3)
        
        assert app.is_dragging
        assert app.drag_start_x == 2
        assert app.drag_start_y == 3
        assert app.dragged_cells == [(2, 3)]

    def test_mouse_enter_during_drag(self):
        """Test that mouse enter adds cells to drag path."""
        app = InteractiveGridApp()
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        
        assert app.is_dragging
        assert (2, 1) in app.dragged_cells
        assert (2, 2) in app.dragged_cells
        assert len(app.dragged_cells) == 3  # (1,1), (2,1), (2,2)

    def test_mouse_enter_without_drag(self):
        """Test that mouse enter without active drag does nothing."""
        app = InteractiveGridApp()
        app.on_cell_mouse_enter(2, 3)
        
        assert not app.is_dragging
        assert app.dragged_cells == []

    def test_mouse_up_completes_drag(self):
        """Test that mouse up completes drag and cycles colors."""
        app = InteractiveGridApp()
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        
        # Before mouse up, cells should be unchanged
        assert app.grid.get_cell(1, 1).color_state == 0
        assert app.grid.get_cell(2, 1).color_state == 0
        assert app.grid.get_cell(2, 2).color_state == 0
        
        app.on_cell_mouse_up(2, 2)
        
        # After mouse up, all dragged cells should be cycled
        assert app.grid.get_cell(1, 1).color_state == 1  # orange
        assert app.grid.get_cell(2, 1).color_state == 1  # orange
        assert app.grid.get_cell(2, 2).color_state == 1  # orange
        
        # Drag state should be reset
        assert not app.is_dragging
        assert app.drag_start_x is None
        assert app.drag_start_y is None
        assert app.dragged_cells == []

    def test_mouse_up_without_drag(self):
        """Test that mouse up without active drag does nothing."""
        app = InteractiveGridApp()
        app.on_cell_mouse_up(2, 3)
        
        assert not app.is_dragging
        assert app.grid.get_cell(2, 3).color_state == 0

    def test_drag_rectangular_area(self):
        """Test dragging across a rectangular area."""
        app = InteractiveGridApp()
        
        # Simulate dragging from (1,1) to (3,3)
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(3, 1)
        app.on_cell_mouse_enter(1, 2)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_enter(3, 2)
        app.on_cell_mouse_enter(1, 3)
        app.on_cell_mouse_enter(2, 3)
        app.on_cell_mouse_enter(3, 3)
        app.on_cell_mouse_up(3, 3)
        
        # All cells in the 3x3 area should be orange
        for x in range(1, 4):
            for y in range(1, 4):
                assert app.grid.get_cell(x, y).color_state == 1

    def test_drag_horizontal_line(self):
        """Test dragging horizontally."""
        app = InteractiveGridApp()
        
        app.on_cell_mouse_down(1, 2)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_enter(3, 2)
        app.on_cell_mouse_up(3, 2)
        
        # Only horizontal cells should be affected
        assert app.grid.get_cell(1, 2).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(3, 2).color_state == 1
        # Other cells should remain black
        assert app.grid.get_cell(1, 1).color_state == 0
        assert app.grid.get_cell(2, 1).color_state == 0

    def test_drag_vertical_line(self):
        """Test dragging vertically."""
        app = InteractiveGridApp()
        
        app.on_cell_mouse_down(2, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_enter(2, 3)
        app.on_cell_mouse_up(2, 3)
        
        # Only vertical cells should be affected
        assert app.grid.get_cell(2, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(2, 3).color_state == 1
        # Other cells should remain black
        assert app.grid.get_cell(1, 2).color_state == 0
        assert app.grid.get_cell(3, 2).color_state == 0

    def test_drag_diagonal_line(self):
        """Test dragging diagonally."""
        app = InteractiveGridApp()
        
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(1, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # Only diagonal cells should be affected
        assert app.grid.get_cell(0, 0).color_state == 1
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1
        # Other cells should remain black
        assert app.grid.get_cell(0, 1).color_state == 0
        assert app.grid.get_cell(1, 0).color_state == 0

    def test_drag_with_existing_colors(self):
        """Test dragging over cells with existing colors."""
        app = InteractiveGridApp()
        
        # Set up some existing colors
        app.grid.get_cell(1, 1).set_color_state(1)  # orange
        app.grid.get_cell(2, 2).set_color_state(2)  # blue
        
        # Drag over these cells
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(1, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # All dragged cells should be cycled
        assert app.grid.get_cell(0, 0).color_state == 1  # black -> orange
        assert app.grid.get_cell(1, 1).color_state == 2  # orange -> blue
        assert app.grid.get_cell(2, 2).color_state == 0  # blue -> black

    def test_drag_boundary_handling(self):
        """Test that drag handles grid boundaries correctly."""
        app = InteractiveGridApp(width=3, height=3)  # Small grid for testing
        
        # Try to drag outside boundaries
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(1, 0)
        app.on_cell_mouse_enter(2, 0)
        app.on_cell_mouse_enter(3, 0)  # Outside grid - should be ignored
        app.on_cell_mouse_up(2, 0)  # Use valid coordinates for mouse up
        
        # Only cells within grid should be affected
        assert app.grid.get_cell(0, 0).color_state == 1
        assert app.grid.get_cell(1, 0).color_state == 1
        assert app.grid.get_cell(2, 0).color_state == 1
        # Cell (3,0) doesn't exist, so no assertion needed

    def test_multiple_drag_operations(self):
        """Test multiple consecutive drag operations."""
        app = InteractiveGridApp()
        
        # First drag
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_up(2, 1)
        
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
        
        # Second drag
        app.on_cell_mouse_down(3, 3)
        app.on_cell_mouse_enter(4, 3)
        app.on_cell_mouse_up(4, 3)
        
        assert app.grid.get_cell(3, 3).color_state == 1
        assert app.grid.get_cell(4, 3).color_state == 1
        # Previous drag should be unchanged
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
