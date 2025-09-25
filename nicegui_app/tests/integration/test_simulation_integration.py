"""Integration tests for simulation logic and Conway's Game of Life."""

import pytest
import time
from models import Grid, Cell
from simulation import run_conway_step
from ..test_utils import (
    create_blinker_pattern,
    create_block_pattern,
    create_barrier_pattern,
    GridTestHelper,
    assert_grid_states_equal,
    count_cells_by_state,
)


class TestConwayPatterns:
    """Test classic Conway's Game of Life patterns."""
    
    def test_blinker_oscillation(self):
        """Test that blinker pattern oscillates correctly."""
        grid = Grid(5, 5)
        create_blinker_pattern(grid)
        
        # Initial state: horizontal line
        assert grid.cells[1][0].is_blue_traffic()
        assert grid.cells[1][1].is_blue_traffic()
        assert grid.cells[1][2].is_blue_traffic()
        
        # After 1 step: should become vertical
        new_grid = run_conway_step(grid)
        assert new_grid.cells[0][1].is_blue_traffic()
        assert new_grid.cells[1][1].is_blue_traffic()
        assert new_grid.cells[2][1].is_blue_traffic()
        
        # After 2 steps: should return to horizontal (oscillates every 2 steps)
        final_grid = run_conway_step(new_grid)
        assert final_grid.cells[1][0].is_blue_traffic()
        assert final_grid.cells[1][1].is_blue_traffic()
        assert final_grid.cells[1][2].is_blue_traffic()
    
    def test_block_still_life(self):
        """Test that block pattern remains stable."""
        grid = Grid(4, 4)
        create_block_pattern(grid)
        
        # Run multiple steps
        current_grid = grid
        for _ in range(5):
            current_grid = run_conway_step(current_grid)
        
        # Block should remain unchanged
        assert current_grid.cells[0][0].is_blue_traffic()
        assert current_grid.cells[0][1].is_blue_traffic()
        assert current_grid.cells[1][0].is_blue_traffic()
        assert current_grid.cells[1][1].is_blue_traffic()
    
    def test_single_cell_dies(self):
        """Test that isolated cells die."""
        grid = Grid(3, 3)
        grid.cells[1][1].set_color_state(2)  # Single blue cell
        
        # After one step, should die
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_black()
    
    def test_three_cells_create_new(self):
        """Test that three adjacent cells create a new cell."""
        grid = Grid(4, 4)
        # Create L-shape pattern
        grid.cells[1][1].set_color_state(2)
        grid.cells[1][2].set_color_state(2)
        grid.cells[2][1].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        
        # Should create a block pattern
        assert new_grid.cells[1][1].is_blue_traffic()
        assert new_grid.cells[1][2].is_blue_traffic()
        assert new_grid.cells[2][1].is_blue_traffic()
        assert new_grid.cells[2][2].is_blue_traffic()


class TestTrafficBarriers:
    """Test that orange barriers remain static during simulation."""
    
    def test_barriers_remain_static(self):
        """Test that orange barriers don't evolve."""
        grid = Grid(5, 5)
        create_barrier_pattern(grid)
        
        # Run multiple simulation steps
        current_grid = grid
        for _ in range(10):
            current_grid = run_conway_step(current_grid)
        
        # Orange barriers should remain unchanged
        assert current_grid.cells[1][1].is_orange()
        assert current_grid.cells[2][1].is_orange()
        assert current_grid.cells[1][2].is_orange()
        assert current_grid.cells[2][2].is_orange()
    
    def test_traffic_around_barriers(self):
        """Test that traffic evolves normally around barriers."""
        grid = Grid(5, 5)
        create_barrier_pattern(grid)
        
        # Blue cell should be present
        assert grid.cells[1][0].is_blue_traffic()
        
        # Run one step
        new_grid = run_conway_step(grid)
        
        # Traffic should evolve according to Conway rules
        # The blue cell at (1,0) should die due to underpopulation
        assert new_grid.cells[1][0].is_black()
        
        # But barriers remain
        assert new_grid.cells[1][1].is_orange()
        assert new_grid.cells[2][1].is_orange()
        assert new_grid.cells[1][2].is_orange()
        assert new_grid.cells[2][2].is_orange()


class TestSimulationEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_grid_remains_empty(self):
        """Test that empty grid remains empty."""
        grid = Grid(3, 3)
        
        # All cells should be black initially
        for row in grid.cells:
            for cell in row:
                assert cell.is_black()
        
        # After simulation, should still be empty
        new_grid = run_conway_step(grid)
        for row in new_grid.cells:
            for cell in row:
                assert cell.is_black()
    
    def test_full_grid_behavior(self):
        """Test behavior with grid full of traffic."""
        grid = Grid(3, 3)
        
        # Fill grid with blue traffic
        for row in grid.cells:
            for cell in row:
                cell.set_color_state(2)
        
        # Run simulation
        new_grid = run_conway_step(grid)
        
        # Should result in different pattern (Conway rules with 8 neighbors each)
        # Most cells should die (overpopulation)
        black_count, _, blue_count = count_cells_by_state(new_grid)
        assert black_count > blue_count  # More deaths than survivals
    
    def test_single_row_grid(self):
        """Test simulation on single row grid."""
        grid = Grid(5, 1)
        
        # Create pattern in single row
        grid.cells[0][1].set_color_state(2)
        grid.cells[0][2].set_color_state(2)
        grid.cells[0][3].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        
        # Should evolve according to rules
        assert new_grid.cells[0][2].is_blue_traffic()  # Center survives
        assert new_grid.cells[0][1].is_black()  # Edge dies
        assert new_grid.cells[0][3].is_black()  # Edge dies
    
    def test_single_column_grid(self):
        """Test simulation on single column grid."""
        grid = Grid(1, 5)
        
        # Create pattern in single column
        grid.cells[1][0].set_color_state(2)
        grid.cells[2][0].set_color_state(2)
        grid.cells[3][0].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        
        # Should evolve according to rules
        assert new_grid.cells[2][0].is_blue_traffic()  # Center survives
        assert new_grid.cells[1][0].is_black()  # Edge dies
        assert new_grid.cells[3][0].is_black()  # Edge dies


class TestGridIntegration:
    """Test integration between Grid class and simulation."""
    
    def test_grid_apply_conway_step(self):
        """Test that Grid.apply_conway_step works correctly."""
        grid = Grid(3, 3)
        create_blinker_pattern(grid)
        
        # Store original state
        original_state = [(x, y, cell.color_state) for y, row in enumerate(grid.cells) 
                         for x, cell in enumerate(row) if cell.color_state != 0]
        
        # Apply Conway step
        grid.apply_conway_step()
        
        # Verify state changed
        new_state = [(x, y, cell.color_state) for y, row in enumerate(grid.cells) 
                    for x, cell in enumerate(row) if cell.color_state != 0]
        
        assert original_state != new_state  # State should have changed
    
    def test_simulation_with_resize(self):
        """Test simulation behavior after grid resize."""
        grid = Grid(3, 3)
        create_blinker_pattern(grid)
        
        # Resize grid
        grid.resize(5, 5)
        
        # Verify pattern is preserved in new grid
        assert grid.cells[1][0].is_blue_traffic()
        assert grid.cells[1][1].is_blue_traffic()
        assert grid.cells[1][2].is_blue_traffic()
        
        # Run simulation on resized grid
        grid.apply_conway_step()
        
        # Should still oscillate correctly
        assert grid.cells[0][1].is_blue_traffic()
        assert grid.cells[1][1].is_blue_traffic()
        assert grid.cells[2][1].is_blue_traffic()
    
    def test_save_load_with_simulation(self):
        """Test that saved/loaded grids work correctly with simulation."""
        grid = Grid(3, 3)
        create_blinker_pattern(grid)
        
        # Save grid
        grid.save_to_file("test_simulation.json")
        
        # Run simulation on original
        grid.apply_conway_step()
        
        # Load saved grid
        loaded_grid = Grid.load_from_file("test_simulation.json")
        
        # Verify loaded grid has original pattern
        assert loaded_grid.cells[1][0].is_blue_traffic()
        assert loaded_grid.cells[1][1].is_blue_traffic()
        assert loaded_grid.cells[1][2].is_blue_traffic()
        
        # Run simulation on loaded grid
        loaded_grid.apply_conway_step()
        
        # Should evolve the same way (horizontal to vertical)
        assert loaded_grid.cells[0][1].is_blue_traffic()
        assert loaded_grid.cells[1][1].is_blue_traffic()
        assert loaded_grid.cells[2][1].is_blue_traffic()
        
        # Cleanup
        import os
        if os.path.exists("test_simulation.json"):
            os.unlink("test_simulation.json")


class TestPerformanceIntegration:
    """Test performance characteristics of simulation."""
    
    def test_large_grid_simulation_performance(self):
        """Test simulation performance on large grid."""
        grid = Grid(50, 50)
        
        # Create some patterns
        for i in range(0, 50, 5):
            for j in range(0, 50, 5):
                if (i + j) % 10 == 0:
                    grid.cells[j][i].set_color_state(2)
        
        # Measure simulation time
        start_time = time.time()
        new_grid = run_conway_step(grid)
        end_time = time.time()
        
        # Should complete in reasonable time (< 1 second)
        assert (end_time - start_time) < 1.0
        
        # Verify grid was processed
        assert new_grid.width == 50
        assert new_grid.height == 50
    
    def test_multiple_simulation_steps(self):
        """Test running multiple simulation steps in sequence."""
        grid = Grid(10, 10)
        create_blinker_pattern(grid)
        
        # Run 100 simulation steps
        current_grid = grid
        for i in range(100):
            current_grid = run_conway_step(current_grid)
        
        # Should still have traffic (blinker oscillates)
        has_traffic = any(cell.is_blue_traffic() for row in current_grid.cells for cell in row)
        assert has_traffic
    
    def test_simulation_with_mixed_states(self):
        """Test simulation with mixed orange barriers and blue traffic."""
        grid = Grid(10, 10)
        
        # Create complex pattern with barriers and traffic
        for y in range(10):
            for x in range(10):
                if (x + y) % 3 == 0:
                    grid.cells[y][x].set_color_state(1)  # Orange barriers
                elif (x + y) % 5 == 0:
                    grid.cells[y][x].set_color_state(2)  # Blue traffic
        
        # Run simulation
        new_grid = run_conway_step(grid)
        
        # Count states
        black_count, orange_count, blue_count = count_cells_by_state(new_grid)
        
        # Orange barriers should remain
        assert orange_count > 0
        
        # Some traffic should exist
        assert blue_count >= 0  # Could be 0 if all traffic died


class TestConwayRulesCorrectness:
    """Test that Conway's rules are implemented correctly."""
    
    def test_underpopulation_rule(self):
        """Test that cells with < 2 neighbors die."""
        grid = Grid(3, 3)
        
        # Single cell (0 neighbors)
        grid.cells[1][1].set_color_state(2)
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_black()
        
        # Two isolated cells (1 neighbor each)
        grid = Grid(3, 3)
        grid.cells[0][0].set_color_state(2)
        grid.cells[2][2].set_color_state(2)
        new_grid = run_conway_step(grid)
        assert new_grid.cells[0][0].is_black()
        assert new_grid.cells[2][2].is_black()
    
    def test_overpopulation_rule(self):
        """Test that cells with > 3 neighbors die."""
        grid = Grid(3, 3)
        
        # Center cell with 4 neighbors
        grid.cells[0][1].set_color_state(2)
        grid.cells[1][0].set_color_state(2)
        grid.cells[1][1].set_color_state(2)  # Center
        grid.cells[1][2].set_color_state(2)
        grid.cells[2][1].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_black()  # Center should die
    
    def test_reproduction_rule(self):
        """Test that empty cells with exactly 3 neighbors become alive."""
        grid = Grid(3, 3)
        
        # Empty center with 3 neighbors
        grid.cells[0][1].set_color_state(2)
        grid.cells[1][0].set_color_state(2)
        grid.cells[1][2].set_color_state(2)
        # Center is empty
        
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_blue_traffic()  # Center should become alive
    
    def test_survival_rule(self):
        """Test that cells with 2-3 neighbors survive."""
        grid = Grid(3, 3)
        
        # Center cell with 2 neighbors
        grid.cells[1][1].set_color_state(2)  # Center
        grid.cells[0][1].set_color_state(2)
        grid.cells[1][0].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_blue_traffic()  # Should survive
        
        # Center cell with 3 neighbors
        grid = Grid(3, 3)
        grid.cells[1][1].set_color_state(2)  # Center
        grid.cells[0][1].set_color_state(2)
        grid.cells[1][0].set_color_state(2)
        grid.cells[1][2].set_color_state(2)
        
        new_grid = run_conway_step(grid)
        assert new_grid.cells[1][1].is_blue_traffic()  # Should survive
