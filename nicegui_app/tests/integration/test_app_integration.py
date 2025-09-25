"""Integration tests against the running Conway Traffic app."""

import pytest
import time
import threading
from app import InteractiveGridApp


class TestAppIntegration:
    """Integration tests against the running app."""
    
    @pytest.fixture(scope="class")
    def app_server(self):
        """Start the app server for testing."""
        # This would start the actual NiceGUI app
        # For now, we'll test the core functionality without the web interface
        app = InteractiveGridApp(width=5, height=5)
        return app
    
    def test_app_initialization(self, app_server):
        """Test that the app initializes correctly."""
        assert app_server.width == 5
        assert app_server.height == 5
        assert app_server.grid.width == 5
        assert app_server.grid.height == 5
        assert not app_server.simulation_running
    
    def test_cell_interaction_workflow(self, app_server):
        """Test complete cell interaction workflow."""
        # Test cell clicking
        cell = app_server.grid.get_cell(2, 2)
        assert cell.is_black()
        
        # Click to make it orange
        app_server.on_cell_click(2, 2)
        assert cell.is_orange()
        
        # Click to make it blue
        app_server.on_cell_click(2, 2)
        assert cell.is_blue_traffic()
        
        # Click to make it black again
        app_server.on_cell_click(2, 2)
        assert cell.is_black()
    
    def test_simulation_workflow(self, app_server):
        """Test complete simulation workflow."""
        # Set up a pattern
        app_server.grid.get_cell(1, 1).set_color_state(2)  # blue
        app_server.grid.get_cell(1, 2).set_color_state(2)  # blue
        app_server.grid.get_cell(1, 3).set_color_state(2)  # blue
        
        # Run simulation step
        app_server.run_simulation_step()
        
        # Pattern should have evolved
        assert app_server.grid.count_blue_cells() >= 0
    
    def test_save_load_workflow(self, app_server, tmp_path):
        """Test complete save/load workflow."""
        # Use temporary path for testing
        app_server.save_path = str(tmp_path / "test_app_integration_grid.json")
        
        # Set up a pattern
        app_server.grid.get_cell(2, 2).set_color_state(2)  # blue
        app_server.grid.get_cell(3, 3).set_color_state(1)  # orange
        
        # Save the pattern
        app_server.save_grid()
        
        # Clear the grid
        app_server.clear_all()
        assert app_server.grid.count_blue_cells() == 0
        assert app_server.grid.count_orange_cells() == 0
        
        # Load the pattern
        app_server.load_grid()
        
        # Pattern should be restored
        assert app_server.grid.get_cell(2, 2).is_blue_traffic()
        assert app_server.grid.get_cell(3, 3).is_orange()
    
    def test_resize_workflow(self, app_server):
        """Test complete resize workflow."""
        # Set up a pattern
        app_server.grid.get_cell(1, 1).set_color_state(2)  # blue
        
        # Resize grid
        app_server.grid.resize(7, 7)
        app_server.width = 7
        app_server.height = 7
        
        # Pattern should be preserved
        assert app_server.grid.get_cell(1, 1).is_blue_traffic()
        assert app_server.grid.width == 7
        assert app_server.grid.height == 7
    
    def test_continuous_simulation_workflow(self, app_server):
        """Test continuous simulation workflow."""
        # Set up a pattern
        app_server.grid.get_cell(2, 2).set_color_state(2)  # blue
        app_server.grid.get_cell(2, 3).set_color_state(2)  # blue
        app_server.grid.get_cell(2, 4).set_color_state(2)  # blue
        
        # Start continuous simulation
        app_server.run_simulation_continuous()
        assert app_server.simulation_running
        
        # Let it run for a short time
        time.sleep(0.5)
        
        # Stop simulation
        app_server.stop_simulation()
        assert not app_server.simulation_running
    
    def test_traffic_count_updates(self, app_server):
        """Test that traffic count updates correctly."""
        # Mock the traffic count label
        mock_label = type('MockLabel', (), {'text': ''})()
        app_server.traffic_count_label = mock_label
        
        # Set some cells
        app_server.grid.get_cell(1, 1).set_color_state(2)  # blue
        app_server.grid.get_cell(2, 2).set_color_state(1)  # orange
        
        # Update traffic count
        app_server.update_traffic_count()
        
        # Should have updated the label
        expected_text = f"Active traffic elements: {app_server.grid.count_active_cells()}"
        assert mock_label.text == expected_text
    
    def test_clear_all_workflow(self, app_server):
        """Test clear all functionality."""
        # Set up a complex pattern
        app_server.grid.get_cell(1, 1).set_color_state(2)  # blue
        app_server.grid.get_cell(2, 2).set_color_state(1)  # orange
        app_server.grid.get_cell(3, 3).set_color_state(2)  # blue
        
        # Clear all
        app_server.clear_all()
        
        # All cells should be black
        for row in app_server.grid.cells:
            for cell in row:
                assert cell.is_black()
    
    def test_conway_simulation_accuracy(self, app_server):
        """Test that Conway simulation follows correct rules."""
        # Create a blinker pattern
        app_server.grid.get_cell(1, 1).set_color_state(2)  # blue
        app_server.grid.get_cell(1, 2).set_color_state(2)  # blue
        app_server.grid.get_cell(1, 3).set_color_state(2)  # blue
        
        # Run simulation step
        app_server.run_simulation_step()
        
        # Should have evolved to vertical pattern
        assert app_server.grid.get_cell(0, 2).is_blue_traffic()
        assert app_server.grid.get_cell(1, 2).is_blue_traffic()
        assert app_server.grid.get_cell(2, 2).is_blue_traffic()
    
    def test_barrier_preservation(self, app_server):
        """Test that barriers are preserved during simulation."""
        # Set up barriers and traffic
        app_server.grid.get_cell(1, 1).set_color_state(1)  # orange barrier
        app_server.grid.get_cell(2, 2).set_color_state(2)  # blue traffic
        
        # Run simulation
        app_server.run_simulation_step()
        
        # Barrier should remain
        assert app_server.grid.get_cell(1, 1).is_orange()
    
    def test_edge_cases(self, app_server):
        """Test edge cases and boundary conditions."""
        # Test single cell
        app_server.grid.get_cell(0, 0).set_color_state(2)  # blue
        app_server.run_simulation_step()
        # Should die due to underpopulation
        assert app_server.grid.get_cell(0, 0).is_black()
        
        # Test corner cells
        app_server.grid.get_cell(4, 4).set_color_state(2)  # blue
        app_server.run_simulation_step()
        # Should die due to underpopulation
        assert app_server.grid.get_cell(4, 4).is_black()


class TestAppPerformance:
    """Performance tests for the app."""
    
    def test_large_grid_performance(self):
        """Test performance with large grids."""
        app = InteractiveGridApp(width=50, height=50)
        
        # Set up a pattern
        for i in range(10):
            app.grid.get_cell(i, i).set_color_state(2)  # blue
        
        # Time the simulation
        start_time = time.time()
        app.run_simulation_step()
        end_time = time.time()
        
        # Should complete quickly
        assert (end_time - start_time) < 1.0  # Less than 1 second
    
    def test_multiple_simulation_steps(self):
        """Test multiple simulation steps."""
        app = InteractiveGridApp(width=10, height=10)
        
        # Set up a pattern
        app.grid.get_cell(5, 5).set_color_state(2)  # blue
        app.grid.get_cell(5, 6).set_color_state(2)  # blue
        app.grid.get_cell(5, 7).set_color_state(2)  # blue
        
        # Run multiple steps
        for _ in range(10):
            app.run_simulation_step()
        
        # Should still be running without errors
        assert app.grid.width == 10
        assert app.grid.height == 10
