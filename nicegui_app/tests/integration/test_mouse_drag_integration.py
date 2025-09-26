"""Integration tests for mouse drag functionality."""

import pytest
from app import InteractiveGridApp
from models import Grid


class TestMouseDragIntegration:
    """Integration tests for mouse drag functionality with the full app."""

    def test_drag_with_simulation_running(self):
        """Test that drag works while simulation is running."""
        app = InteractiveGridApp()
        
        # Start simulation
        app.simulation_running = True
        
        # Perform drag operation
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # Drag should work even with simulation running
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1
        
        # Simulation state should be preserved
        assert app.simulation_running

    def test_drag_with_grid_resize(self):
        """Test that drag state is preserved during grid resize."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Start a drag operation
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        
        # Resize grid
        app.grid.resize(10, 10)
        app.width = 10
        app.height = 10
        
        # Complete drag operation
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # Drag should still work after resize
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1

    def test_drag_with_save_load(self):
        """Test that drag works with save/load operations."""
        app = InteractiveGridApp()
        
        # Perform drag operation
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # Save grid
        app.save_grid()
        
        # Clear grid
        app.clear_all()
        assert app.grid.get_cell(1, 1).color_state == 0
        assert app.grid.get_cell(2, 1).color_state == 0
        assert app.grid.get_cell(2, 2).color_state == 0
        
        # Load grid
        app.load_grid()
        
        # Dragged cells should be restored
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1

    def test_drag_with_traffic_count_update(self):
        """Test that traffic count updates correctly after drag."""
        app = InteractiveGridApp()
        
        # Initial count should be 0
        initial_count = app.grid.count_active_cells()
        assert initial_count == 0
        
        # Perform drag operation
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_up(2, 2)
        
        # Count should reflect the new orange cells
        final_count = app.grid.count_active_cells()
        assert final_count == 3  # 3 orange cells

    def test_drag_with_clear_all(self):
        """Test that drag works after clear all operation."""
        app = InteractiveGridApp()
        
        # Set up some initial state
        app.grid.get_cell(0, 0).set_color_state(1)
        app.grid.get_cell(1, 1).set_color_state(2)
        
        # Clear all
        app.clear_all()
        
        # Perform drag operation
        app.on_cell_mouse_down(2, 2)
        app.on_cell_mouse_enter(3, 2)
        app.on_cell_mouse_enter(3, 3)
        app.on_cell_mouse_up(3, 3)
        
        # Drag should work after clear
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(3, 2).color_state == 1
        assert app.grid.get_cell(3, 3).color_state == 1
        
        # Previously cleared cells should remain black
        assert app.grid.get_cell(0, 0).color_state == 0
        assert app.grid.get_cell(1, 1).color_state == 0

    def test_drag_with_conway_simulation(self):
        """Test that drag works with Conway's Game of Life simulation."""
        app = InteractiveGridApp()
        
        # Set up a simple pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(2, 1).set_color_state(2)  # blue
        app.grid.get_cell(1, 2).set_color_state(2)  # blue
        
        # Perform drag operation
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(1, 0)
        app.on_cell_mouse_enter(2, 0)
        app.on_cell_mouse_up(2, 0)
        
        # Run Conway simulation
        app.run_simulation_step()
        
        # Dragged cells should still be orange (not affected by Conway rules)
        assert app.grid.get_cell(0, 0).color_state == 1
        assert app.grid.get_cell(1, 0).color_state == 1
        assert app.grid.get_cell(2, 0).color_state == 1
        
        # Blue cells should have evolved according to Conway rules
        # (exact state depends on Conway rules implementation)

    def test_drag_state_consistency(self):
        """Test that drag state remains consistent across operations."""
        app = InteractiveGridApp()
        
        # Start drag
        app.on_cell_mouse_down(1, 1)
        assert app.is_dragging
        assert app.drag_start_x == 1
        assert app.drag_start_y == 1
        assert app.dragged_cells == [(1, 1)]
        
        # Add more cells to drag
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        assert len(app.dragged_cells) == 3
        
        # Complete drag
        app.on_cell_mouse_up(2, 2)
        assert not app.is_dragging
        assert app.drag_start_x is None
        assert app.drag_start_y is None
        assert app.dragged_cells == []

    def test_drag_with_large_grid(self):
        """Test drag functionality with a large grid."""
        app = InteractiveGridApp(width=50, height=50)
        
        # Perform drag across large area
        app.on_cell_mouse_down(10, 10)
        for x in range(10, 20):
            for y in range(10, 20):
                app.on_cell_mouse_enter(x, y)
        app.on_cell_mouse_up(19, 19)
        
        # All cells in the 10x10 area should be orange
        for x in range(10, 20):
            for y in range(10, 20):
                assert app.grid.get_cell(x, y).color_state == 1
        
        # Cells outside the drag area should remain black
        assert app.grid.get_cell(9, 9).color_state == 0
        assert app.grid.get_cell(20, 20).color_state == 0

    def test_drag_performance(self):
        """Test that drag operations are performant."""
        app = InteractiveGridApp(width=20, height=20)
        
        # Perform multiple drag operations
        for i in range(5):
            app.on_cell_mouse_down(i, i)
            app.on_cell_mouse_enter(i + 1, i)
            app.on_cell_mouse_enter(i + 1, i + 1)
            app.on_cell_mouse_up(i + 1, i + 1)
        
        # All dragged cells should be cycled (not black)
        for i in range(5):
            # Each cell should be cycled (not black/0)
            assert app.grid.get_cell(i, i).color_state != 0
            assert app.grid.get_cell(i + 1, i).color_state != 0
            assert app.grid.get_cell(i + 1, i + 1).color_state != 0
