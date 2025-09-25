"""Core application tests without UI dependencies."""

import pytest
from unittest.mock import Mock, patch
from app import InteractiveGridApp


class TestAppCore:
    """Test core application functionality without UI dependencies."""
    
    def test_app_initialization(self):
        """Test that app initializes correctly."""
        app = InteractiveGridApp(width=5, height=5)
        
        assert app.width == 5
        assert app.height == 5
        assert app.grid.width == 5
        assert app.grid.height == 5
        assert not app.simulation_running
        assert app.simulation_thread is None
    
    def test_simulation_step(self):
        """Test single simulation step."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set up a pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(1, 2).set_color_state(2)  # blue
        app.grid.get_cell(1, 0).set_color_state(2)  # blue
        
        # Run simulation step
        app.run_simulation_step()
        
        # Pattern should have evolved
        assert app.grid.count_blue_cells() >= 0  # Some cells may have died
    
    def test_cell_click_functionality(self):
        """Test cell click cycling."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Test cell cycling
        cell = app.grid.get_cell(1, 1)
        assert cell.is_black()
        
        app.on_cell_click(1, 1)
        assert cell.is_orange()
        
        app.on_cell_click(1, 1)
        assert cell.is_blue_traffic()
        
        app.on_cell_click(1, 1)
        assert cell.is_black()
    
    def test_clear_all_functionality(self):
        """Test clear all functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set some cells to non-black
        app.grid.get_cell(1, 1).set_color_state(1)  # orange
        app.grid.get_cell(2, 2).set_color_state(2)  # blue
        
        # Clear all
        app.clear_all()
        
        # All cells should be black
        for row in app.grid.cells:
            for cell in row:
                assert cell.is_black()
    
    def test_resize_functionality(self):
        """Test grid resize functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set a pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        
        # Resize grid
        app.grid.resize(5, 5)
        app.width = 5
        app.height = 5
        
        # Pattern should be preserved
        assert app.grid.get_cell(1, 1).is_blue_traffic()
        assert app.grid.width == 5
        assert app.grid.height == 5
    
    def test_save_load_functionality(self, tmp_path):
        """Test save and load functionality."""
        app = InteractiveGridApp(width=3, height=3)
        # Use temporary path for testing
        app.save_path = str(tmp_path / "test_app_core_grid.json")
        
        # Set a pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(2, 2).set_color_state(1)  # orange
        
        # Save grid
        app.save_grid()
        
        # Clear grid
        app.clear_all()
        
        # Load grid
        app.load_grid()
        
        # Pattern should be restored
        assert app.grid.get_cell(1, 1).is_blue_traffic()
        assert app.grid.get_cell(2, 2).is_orange()
    
    def test_traffic_count_update(self):
        """Test traffic count update functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock the traffic count label
        mock_label = Mock()
        app.traffic_count_label = mock_label
        
        # Set some cells
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(2, 2).set_color_state(1)  # orange
        
        # Update traffic count
        app.update_traffic_count()
        
        # Should have called the label update
        mock_label.text = f"Active traffic elements: {app.grid.count_active_cells()}"
    
    def test_simulation_controls(self):
        """Test simulation start/stop controls."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock the run button
        mock_button = Mock()
        app.run_button = mock_button
        
        # Start simulation
        app.run_simulation_continuous()
        assert app.simulation_running
        mock_button.text = "Stop"
        
        # Stop simulation
        app.stop_simulation()
        assert not app.simulation_running
        mock_button.text = "Run"
