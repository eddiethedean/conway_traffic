"""Unit tests for mouse drag edge cases and error handling."""

import pytest
from app import InteractiveGridApp


class TestMouseDragEdgeCases:
    """Test edge cases and error handling for mouse drag functionality."""

    def test_drag_with_negative_coordinates(self):
        """Test drag behavior with negative coordinates."""
        app = InteractiveGridApp()
        
        # Try to drag with negative coordinates
        app.on_cell_mouse_down(-1, -1)
        app.on_cell_mouse_enter(0, 0)
        app.on_cell_mouse_up(0, 0)
        
        # Should handle gracefully - only valid coordinates should be affected
        # The negative coordinates should be ignored, only (0,0) should be affected
        assert app.grid.get_cell(0, 0).color_state == 1

    def test_drag_with_out_of_bounds_coordinates(self):
        """Test drag behavior with coordinates outside grid bounds."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Try to drag with coordinates outside grid
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(10, 10)  # Outside grid
        app.on_cell_mouse_up(10, 10)
        
        # Should handle gracefully - only valid coordinates should be affected
        # The out-of-bounds coordinates should be ignored, only (0,0) should be affected
        assert app.grid.get_cell(0, 0).color_state == 1

    def test_drag_with_duplicate_cells(self):
        """Test drag behavior when same cell is entered multiple times."""
        app = InteractiveGridApp()
        
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 1)  # Duplicate
        app.on_cell_mouse_enter(2, 1)  # Duplicate again
        app.on_cell_mouse_up(2, 1)
        
        # Should only cycle each cell once
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1

    def test_drag_with_rapid_mouse_events(self):
        """Test drag behavior with rapid mouse events."""
        app = InteractiveGridApp()
        
        # Rapid sequence of mouse events
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        app.on_cell_mouse_enter(1, 2)
        app.on_cell_mouse_enter(1, 1)  # Back to start
        app.on_cell_mouse_up(1, 1)
        
        # Should handle rapid events correctly
        assert app.grid.get_cell(1, 1).color_state == 1
        assert app.grid.get_cell(2, 1).color_state == 1
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(1, 2).color_state == 1

    def test_drag_with_interrupted_sequence(self):
        """Test drag behavior when mouse sequence is interrupted."""
        app = InteractiveGridApp()
        
        # Start drag but don't complete it
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        app.on_cell_mouse_enter(2, 2)
        
        # Start new drag without completing first
        app.on_cell_mouse_down(3, 3)
        app.on_cell_mouse_enter(4, 3)
        app.on_cell_mouse_up(4, 3)
        
        # Only the second drag should be completed
        assert app.grid.get_cell(1, 1).color_state == 0  # First drag not completed
        assert app.grid.get_cell(2, 1).color_state == 0
        assert app.grid.get_cell(2, 2).color_state == 0
        assert app.grid.get_cell(3, 3).color_state == 1  # Second drag completed
        assert app.grid.get_cell(4, 3).color_state == 1

    def test_drag_with_single_cell(self):
        """Test drag behavior with single cell (no movement)."""
        app = InteractiveGridApp()
        
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_up(1, 1)  # No movement
        
        # Single cell should still be cycled
        assert app.grid.get_cell(1, 1).color_state == 1

    def test_drag_with_zero_size_grid(self):
        """Test drag behavior with zero-size grid."""
        # Zero-size grid should raise an error during initialization
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            app = InteractiveGridApp(width=0, height=0)

    def test_drag_with_one_cell_grid(self):
        """Test drag behavior with 1x1 grid."""
        app = InteractiveGridApp(width=1, height=1)
        
        app.on_cell_mouse_down(0, 0)
        app.on_cell_mouse_enter(0, 0)  # Same cell
        app.on_cell_mouse_up(0, 0)
        
        # Should cycle the single cell
        assert app.grid.get_cell(0, 0).color_state == 1

    def test_drag_with_maximum_coordinates(self):
        """Test drag behavior with maximum valid coordinates."""
        app = InteractiveGridApp(width=10, height=10)
        
        # Use maximum valid coordinates
        app.on_cell_mouse_down(9, 9)
        app.on_cell_mouse_enter(8, 9)
        app.on_cell_mouse_enter(8, 8)
        app.on_cell_mouse_up(8, 8)
        
        # Should work with maximum coordinates
        assert app.grid.get_cell(9, 9).color_state == 1
        assert app.grid.get_cell(8, 9).color_state == 1
        assert app.grid.get_cell(8, 8).color_state == 1

    def test_drag_with_mixed_valid_invalid_coordinates(self):
        """Test drag behavior with mix of valid and invalid coordinates."""
        app = InteractiveGridApp(width=5, height=5)
        
        app.on_cell_mouse_down(2, 2)
        app.on_cell_mouse_enter(3, 2)  # Valid
        app.on_cell_mouse_enter(10, 2)  # Invalid - should be ignored
        app.on_cell_mouse_enter(3, 3)  # Valid
        app.on_cell_mouse_enter(-1, 3)  # Invalid - should be ignored
        app.on_cell_mouse_up(3, 3)
        
        # Only valid coordinates should be affected
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(3, 2).color_state == 1
        assert app.grid.get_cell(3, 3).color_state == 1

    def test_drag_state_reset_after_error(self):
        """Test that drag state is reset after error conditions."""
        app = InteractiveGridApp()
        
        # Start drag
        app.on_cell_mouse_down(1, 1)
        assert app.is_dragging
        
        # Simulate error condition (e.g., grid corruption)
        # Reset drag state manually
        app.is_dragging = False
        app.drag_start_x = None
        app.drag_start_y = None
        app.dragged_cells = []
        
        # New drag should work normally
        app.on_cell_mouse_down(2, 2)
        app.on_cell_mouse_enter(3, 2)
        app.on_cell_mouse_up(3, 2)
        
        assert app.grid.get_cell(2, 2).color_state == 1
        assert app.grid.get_cell(3, 2).color_state == 1

    def test_drag_with_concurrent_operations(self):
        """Test drag behavior with concurrent operations."""
        app = InteractiveGridApp()
        
        # Start drag
        app.on_cell_mouse_down(1, 1)
        app.on_cell_mouse_enter(2, 1)
        
        # Perform other operations during drag
        app.grid.cycle_cell_color(5, 5)  # Manual cell change
        app.clear_all()  # Clear all during drag
        
        # Complete drag
        app.on_cell_mouse_up(2, 1)
        
        # After clear_all, the drag should still complete but on the cleared grid
        # The drag operation should still work, but the cells were cleared
        assert app.grid.get_cell(1, 1).color_state == 1  # Drag completed after clear
        assert app.grid.get_cell(2, 1).color_state == 1  # Drag completed after clear
        assert app.grid.get_cell(5, 5).color_state == 0  # Cleared
