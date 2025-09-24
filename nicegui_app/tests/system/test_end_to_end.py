"""End-to-end system tests for complete user workflows."""

import pytest
from unittest.mock import Mock, patch
from app import InteractiveGridApp


class TestCompleteUserWorkflow:
    """Test complete user workflows from start to finish."""
    
    @patch('app.ui')
    def test_create_pattern_save_and_load_workflow(self, mock_ui):
        """Test complete workflow: create pattern, save, clear, load."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Create pattern
        app.on_cell_click(1, 1)  # orange
        app.on_cell_click(1, 1)  # blue
        app.on_cell_click(0, 0)  # orange
        
        # Save pattern
        app.save_grid()
        
        # Clear grid
        app.clear_all()
        assert app.grid.count_active_cells() == 0
        
        # Load pattern
        app.load_grid()
        assert app.grid.count_active_cells() == 2
    
    @patch('app.ui')
    def test_resize_and_simulation_workflow(self, mock_ui):
        """Test workflow: resize grid, create pattern, run simulation."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_width_input = Mock()
        mock_width_input.value = 5
        mock_height_input = Mock()
        mock_height_input.value = 5
        app.width_input = mock_width_input
        app.height_input = mock_height_input
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Resize grid
        app.resize_grid()
        assert app.grid.width == 5
        assert app.grid.height == 5
        
        # Create blinker pattern
        app.on_cell_click(2, 2)  # orange
        app.on_cell_click(2, 2)  # blue
        app.on_cell_click(1, 2)  # orange
        app.on_cell_click(1, 2)  # blue
        app.on_cell_click(3, 2)  # orange
        app.on_cell_click(3, 2)  # blue
        
        # Run simulation
        app.run_simulation_step()
        assert app.grid.count_active_cells() == 3  # Blinker oscillates
    
    @patch('app.ui')
    def test_continuous_simulation_workflow(self, mock_ui):
        """Test continuous simulation start/stop workflow."""
        app = InteractiveGridApp(width=3, height=3)
        
        mock_run_button = Mock()
        app.run_button = mock_run_button
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Start simulation
        app.toggle_simulation()
        assert app.simulation_running
        assert app.run_button.text == "Stop"
        
        # Stop simulation
        app.toggle_simulation()
        assert not app.simulation_running
        assert app.run_button.text == "Run"
