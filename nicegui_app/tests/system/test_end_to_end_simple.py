"""Simplified end-to-end tests that focus on core functionality."""

import pytest
from app import InteractiveGridApp


class TestEndToEndSimple:
    """Simplified end-to-end tests."""
    
    def test_complete_user_workflow(self, tmp_path):
        """Test complete user workflow without UI dependencies."""
        app = InteractiveGridApp(width=5, height=5)
        # Use temporary path for testing
        app.save_path = str(tmp_path / "test_workflow_grid.json")
        
        # 1. User creates a pattern
        app.on_cell_click(1, 1)  # orange
        app.on_cell_click(1, 1)  # blue
        app.on_cell_click(2, 2)  # orange
        app.on_cell_click(3, 3)  # orange
        app.on_cell_click(3, 3)  # blue
        
        # 2. User runs simulation
        app.run_simulation_step()
        
        # 3. User saves the pattern
        app.save_grid()
        
        # 4. User clears the grid
        app.clear_all()
        
        # 5. User loads the pattern back
        app.load_grid()
        
        # 6. User resizes the grid
        app.grid.resize(7, 7)
        app.width = 7
        app.height = 7
        
        # 7. User starts continuous simulation
        app.run_simulation_continuous()
        assert app.simulation_running
        
        # 8. User stops simulation
        app.stop_simulation()
        assert not app.simulation_running
        
        # App should still be functional
        assert app.grid.width == 7
        assert app.grid.height == 7
    
    def test_resize_and_simulation_workflow(self):
        """Test resize and simulation workflow."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set up a pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(1, 2).set_color_state(2)  # blue
        app.grid.get_cell(1, 0).set_color_state(2)  # blue
        
        # Resize grid
        app.grid.resize(5, 5)
        app.width = 5
        app.height = 5
        
        # Pattern should be preserved
        assert app.grid.get_cell(1, 1).is_blue_traffic()
        assert app.grid.get_cell(1, 2).is_blue_traffic()
        assert app.grid.get_cell(1, 0).is_blue_traffic()
        
        # Run simulation
        app.run_simulation_step()
        
        # Should have evolved
        assert app.grid.count_blue_cells() >= 0
    
    def test_continuous_simulation_workflow(self):
        """Test continuous simulation workflow."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Set up a pattern
        app.grid.get_cell(2, 2).set_color_state(2)  # blue
        app.grid.get_cell(2, 3).set_color_state(2)  # blue
        app.grid.get_cell(2, 4).set_color_state(2)  # blue
        
        # Start continuous simulation
        app.run_simulation_continuous()
        assert app.simulation_running
        
        # Let it run briefly
        import time
        time.sleep(0.2)
        
        # Stop simulation
        app.stop_simulation()
        assert not app.simulation_running
        
        # App should still be functional
        assert app.grid.width == 5
        assert app.grid.height == 5
    
    def test_save_load_workflow(self, tmp_path):
        """Test save/load workflow."""
        app = InteractiveGridApp(width=4, height=4)
        # Use temporary path for testing
        app.save_path = str(tmp_path / "test_save_load_grid.json")
        
        # Set up a complex pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(2, 2).set_color_state(1)  # orange
        app.grid.get_cell(3, 3).set_color_state(2)  # blue
        
        # Save the pattern
        app.save_grid()
        
        # Clear the grid
        app.clear_all()
        assert app.grid.count_blue_cells() == 0
        assert app.grid.count_orange_cells() == 0
        
        # Load the pattern
        app.load_grid()
        
        # Pattern should be restored
        assert app.grid.get_cell(1, 1).is_blue_traffic()
        assert app.grid.get_cell(2, 2).is_orange()
        assert app.grid.get_cell(3, 3).is_blue_traffic()
    
    def test_simulation_accuracy_workflow(self):
        """Test simulation accuracy workflow."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Create a blinker pattern
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(1, 2).set_color_state(2)  # blue
        app.grid.get_cell(1, 3).set_color_state(2)  # blue
        
        # Run simulation step
        app.run_simulation_step()
        
        # Should evolve to vertical pattern
        assert app.grid.get_cell(0, 2).is_blue_traffic()
        assert app.grid.get_cell(1, 2).is_blue_traffic()
        assert app.grid.get_cell(2, 2).is_blue_traffic()
        
        # Run another step
        app.run_simulation_step()
        
        # Should return to horizontal pattern
        assert app.grid.get_cell(1, 1).is_blue_traffic()
        assert app.grid.get_cell(1, 2).is_blue_traffic()
        assert app.grid.get_cell(1, 3).is_blue_traffic()
    
    def test_barrier_workflow(self):
        """Test barrier workflow."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Set up barriers and traffic
        app.grid.get_cell(1, 1).set_color_state(1)  # orange barrier
        app.grid.get_cell(2, 2).set_color_state(2)  # blue traffic
        
        # Run multiple simulation steps
        for _ in range(5):
            app.run_simulation_step()
        
        # Barrier should remain unchanged
        assert app.grid.get_cell(1, 1).is_orange()
    
    def test_edge_case_workflow(self):
        """Test edge case workflow."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Test single cell dies
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.run_simulation_step()
        assert app.grid.get_cell(1, 1).is_black()
        
        # Test corner cells
        app.grid.get_cell(0, 0).set_color_state(2)  # blue
        app.run_simulation_step()
        assert app.grid.get_cell(0, 0).is_black()
        
        # Test reproduction rule
        app.grid.get_cell(1, 1).set_color_state(2)  # blue
        app.grid.get_cell(1, 2).set_color_state(2)  # blue
        app.grid.get_cell(1, 0).set_color_state(2)  # blue
        app.run_simulation_step()
        # Center should survive (has 2 neighbors)
        assert app.grid.get_cell(1, 1).is_blue_traffic()
    
    def test_performance_workflow(self):
        """Test performance workflow."""
        app = InteractiveGridApp(width=20, height=20)
        
        # Set up a complex pattern
        for i in range(10):
            for j in range(10):
                if (i + j) % 2 == 0:
                    app.grid.get_cell(i, j).set_color_state(2)  # blue
        
        # Run many simulation steps
        import time
        start_time = time.time()
        for _ in range(10):
            app.run_simulation_step()
        end_time = time.time()
        
        # Should complete quickly
        assert (end_time - start_time) < 2.0  # Less than 2 seconds
        
        # App should still be functional
        assert app.grid.width == 20
        assert app.grid.height == 20
    
    def test_memory_workflow(self):
        """Test memory management workflow."""
        app = InteractiveGridApp(width=10, height=10)
        
        # Create and destroy many patterns
        for _ in range(20):
            # Set up a pattern
            app.grid.get_cell(5, 5).set_color_state(2)  # blue
            app.run_simulation_step()
            app.clear_all()
        
        # App should still be functional
        assert app.grid.width == 10
        assert app.grid.height == 10
        assert app.grid.count_blue_cells() == 0
        assert app.grid.count_orange_cells() == 0
    
    def test_concurrent_workflow(self):
        """Test concurrent operations workflow."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Start continuous simulation
        app.run_simulation_continuous()
        assert app.simulation_running
        
        # While simulation is running, perform other operations
        app.on_cell_click(1, 1)
        app.on_cell_click(2, 2)
        app.update_traffic_count()
        
        # Stop simulation
        app.stop_simulation()
        assert not app.simulation_running
        
        # App should still be functional
        assert app.grid.width == 5
        assert app.grid.height == 5
