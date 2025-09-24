"""Comprehensive unit tests for the Grid model."""

import pytest
import tempfile
import os
from models import Grid, Cell
from ..test_utils import (
    create_blinker_pattern,
    create_block_pattern,
    create_barrier_pattern,
    GridTestHelper,
    assert_grid_states_equal,
    count_cells_by_state,
)


class TestGridInitialization:
    """Test grid initialization and basic properties."""
    
    def test_grid_initialization_default(self):
        """Test grid initialization with default parameters."""
        grid = Grid(5, 3)
        assert grid.width == 5
        assert grid.height == 3
        assert len(grid.cells) == 3
        assert len(grid.cells[0]) == 5
    
    def test_grid_initialization_square(self):
        """Test square grid initialization."""
        grid = Grid(4, 4)
        assert grid.width == 4
        assert grid.height == 4
        assert len(grid.cells) == 4
        assert len(grid.cells[0]) == 4
    
    def test_grid_initialization_single_cell(self):
        """Test single cell grid initialization."""
        grid = Grid(1, 1)
        assert grid.width == 1
        assert grid.height == 1
        assert len(grid.cells) == 1
        assert len(grid.cells[0]) == 1
    
    def test_grid_cells_initialized_correctly(self):
        """Test that all cells are initialized with correct coordinates."""
        grid = Grid(3, 2)
        
        for y in range(2):
            for x in range(3):
                cell = grid.cells[y][x]
                assert cell.x == x
                assert cell.y == y
                assert cell.color_state == 0  # All start black
                assert cell.is_black()
    
    def test_grid_initialization_with_zero_dimensions_raises_error(self):
        """Test that zero dimensions raise ValueError."""
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            Grid(0, 5)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            Grid(5, 0)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            Grid(0, 0)


class TestGridCellAccess:
    """Test cell access and retrieval."""
    
    def test_get_cell_valid_coordinates(self):
        """Test getting cells with valid coordinates."""
        grid = Grid(3, 3)
        
        cell = grid.get_cell(1, 1)
        assert cell.x == 1
        assert cell.y == 1
        assert isinstance(cell, Cell)
    
    def test_get_cell_boundary_coordinates(self):
        """Test getting cells at grid boundaries."""
        grid = Grid(3, 3)
        
        # Top-left corner
        cell = grid.get_cell(0, 0)
        assert cell.x == 0
        assert cell.y == 0
        
        # Bottom-right corner
        cell = grid.get_cell(2, 2)
        assert cell.x == 2
        assert cell.y == 2
    
    def test_get_cell_invalid_coordinates_raises_error(self):
        """Test that invalid coordinates raise IndexError."""
        grid = Grid(3, 3)
        
        # Negative coordinates
        with pytest.raises(IndexError):
            grid.get_cell(-1, 1)
        
        with pytest.raises(IndexError):
            grid.get_cell(1, -1)
        
        # Out of bounds coordinates
        with pytest.raises(IndexError):
            grid.get_cell(3, 1)  # width is 3, so max x is 2
        
        with pytest.raises(IndexError):
            grid.get_cell(1, 3)  # height is 3, so max y is 2
    
    def test_get_cell_large_coordinates_raises_error(self):
        """Test that very large coordinates raise IndexError."""
        grid = Grid(3, 3)
        
        with pytest.raises(IndexError):
            grid.get_cell(100, 1)
        
        with pytest.raises(IndexError):
            grid.get_cell(1, 100)


class TestGridCellOperations:
    """Test cell manipulation operations."""
    
    def test_cycle_cell_color(self):
        """Test cycling cell colors through all states."""
        grid = Grid(3, 3)
        
        # Test cycling through all states
        cell = grid.get_cell(1, 1)
        
        # Initial: black
        assert cell.is_black()
        
        # First cycle: black -> orange
        grid.cycle_cell_color(1, 1)
        assert cell.is_orange()
        
        # Second cycle: orange -> blue
        grid.cycle_cell_color(1, 1)
        assert cell.is_blue_traffic()
        
        # Third cycle: blue -> black
        grid.cycle_cell_color(1, 1)
        assert cell.is_black()
    
    def test_toggle_cell_legacy(self):
        """Test legacy toggle cell functionality."""
        grid = Grid(3, 3)
        
        cell = grid.get_cell(1, 1)
        
        # Initial: black
        assert cell.is_black()
        
        # Toggle: black -> orange
        grid.toggle_cell(1, 1)
        assert cell.is_orange()
        
        # Toggle: orange -> black
        grid.toggle_cell(1, 1)
        assert cell.is_black()
    
    def test_multiple_cell_operations(self):
        """Test operations on multiple cells."""
        grid = Grid(3, 3)
        
        # Set different states for different cells
        grid.cycle_cell_color(0, 0)  # black -> orange
        grid.cycle_cell_color(1, 1)  # black -> orange
        grid.cycle_cell_color(2, 2)  # black -> orange
        grid.cycle_cell_color(2, 2)  # orange -> blue
        
        # Verify states
        assert grid.get_cell(0, 0).is_orange()
        assert grid.get_cell(1, 1).is_orange()
        assert grid.get_cell(2, 2).is_blue_traffic()
        
        # Other cells should remain black
        assert grid.get_cell(0, 1).is_black()
        assert grid.get_cell(1, 0).is_black()


class TestGridResize:
    """Test grid resizing functionality."""
    
    def test_resize_grow_grid(self):
        """Test resizing to larger grid."""
        grid = Grid(2, 2)
        
        # Set some cell states
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        
        # Resize to larger grid
        grid.resize(4, 4)
        
        # Verify new dimensions
        assert grid.width == 4
        assert grid.height == 4
        
        # Verify existing cells preserved
        assert grid.get_cell(0, 0).is_orange()
        assert grid.get_cell(1, 1).is_orange()
        
        # Verify new cells are black
        assert grid.get_cell(2, 2).is_black()
        assert grid.get_cell(3, 3).is_black()
    
    def test_resize_shrink_grid(self):
        """Test resizing to smaller grid."""
        grid = Grid(4, 4)
        
        # Set some cell states
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        grid.cycle_cell_color(3, 3)  # orange (will be lost)
        
        # Resize to smaller grid
        grid.resize(2, 2)
        
        # Verify new dimensions
        assert grid.width == 2
        assert grid.height == 2
        
        # Verify preserved cells
        assert grid.get_cell(0, 0).is_orange()
        assert grid.get_cell(1, 1).is_orange()
    
    def test_resize_same_size(self):
        """Test resizing to same size."""
        grid = Grid(3, 3)
        grid.cycle_cell_color(1, 1)
        
        # Resize to same dimensions
        grid.resize(3, 3)
        
        # Verify nothing changed
        assert grid.width == 3
        assert grid.height == 3
        assert grid.get_cell(1, 1).is_orange()
    
    def test_resize_invalid_dimensions_raises_error(self):
        """Test that invalid resize dimensions raise ValueError."""
        grid = Grid(3, 3)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            grid.resize(0, 3)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            grid.resize(3, 0)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            grid.resize(-1, 3)


class TestGridClearOperations:
    """Test grid clearing functionality."""
    
    def test_clear_all(self):
        """Test clearing all cells."""
        grid = Grid(3, 3)
        
        # Set some cells to different states
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        grid.cycle_cell_color(2, 2)  # orange
        grid.cycle_cell_color(2, 2)  # blue
        
        # Clear all
        grid.clear_all()
        
        # Verify all cells are black
        for row in grid.cells:
            for cell in row:
                assert cell.is_black()
                assert cell.color_state == 0
    
    def test_clear_all_empty_grid(self):
        """Test clearing already empty grid."""
        grid = Grid(3, 3)
        
        # Clear all (should be no-op)
        grid.clear_all()
        
        # Verify all cells still black
        for row in grid.cells:
            for cell in row:
                assert cell.is_black()


class TestGridCounting:
    """Test cell counting functionality."""
    
    def test_count_active_cells(self):
        """Test counting active cells (orange + blue)."""
        grid = Grid(3, 3)
        
        # Initially no active cells
        assert grid.count_active_cells() == 0
        
        # Add some active cells
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        grid.cycle_cell_color(2, 2)  # orange
        grid.cycle_cell_color(2, 2)  # blue
        
        # Should count 3 active cells (2 orange + 1 blue)
        assert grid.count_active_cells() == 3
    
    def test_count_orange_cells(self):
        """Test counting orange cells specifically."""
        grid = Grid(3, 3)
        
        # Initially no orange cells
        assert grid.count_orange_cells() == 0
        
        # Add some orange cells
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        
        # Add a blue cell
        grid.cycle_cell_color(2, 2)  # orange
        grid.cycle_cell_color(2, 2)  # blue
        
        # Should count 2 orange cells
        assert grid.count_orange_cells() == 2
    
    def test_count_blue_cells(self):
        """Test counting blue cells specifically."""
        grid = Grid(3, 3)
        
        # Initially no blue cells
        assert grid.count_blue_cells() == 0
        
        # Add some blue cells
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(0, 0)  # blue
        grid.cycle_cell_color(1, 1)  # orange
        grid.cycle_cell_color(1, 1)  # blue
        
        # Add an orange cell
        grid.cycle_cell_color(2, 2)  # orange
        
        # Should count 2 blue cells
        assert grid.count_blue_cells() == 2


class TestGridSerialization:
    """Test grid serialization and deserialization."""
    
    def test_to_dict_basic(self):
        """Test basic grid to dictionary conversion."""
        grid = Grid(2, 2)
        
        # Set some cell states
        grid.cycle_cell_color(0, 0)  # orange
        grid.cycle_cell_color(1, 1)  # orange
        grid.cycle_cell_color(1, 1)  # blue
        
        data = grid.to_dict()
        
        # Verify structure
        assert data["width"] == 2
        assert data["height"] == 2
        assert len(data["cells"]) == 2
        assert len(data["cells"][0]) == 2
        
        # Verify cell data
        assert data["cells"][0][0]["color_state"] == 1  # orange
        assert data["cells"][1][1]["color_state"] == 2  # blue
        assert data["cells"][0][1]["color_state"] == 0  # black
    
    def test_from_dict_basic(self):
        """Test basic grid creation from dictionary."""
        data = {
            "width": 2,
            "height": 2,
            "cells": [
                [{"color_state": 1}, {"color_state": 0}],
                [{"color_state": 0}, {"color_state": 2}]
            ]
        }
        
        grid = Grid.from_dict(data)
        
        # Verify dimensions
        assert grid.width == 2
        assert grid.height == 2
        
        # Verify cell states
        assert grid.get_cell(0, 0).is_orange()
        assert grid.get_cell(0, 1).is_black()
        assert grid.get_cell(1, 0).is_black()
        assert grid.get_cell(1, 1).is_blue_traffic()
    
    def test_serialization_roundtrip(self):
        """Test that serialization and deserialization preserve state."""
        original_grid = Grid(3, 3)
        
        # Set up complex pattern
        create_barrier_pattern(original_grid)
        
        # Serialize and deserialize
        data = original_grid.to_dict()
        restored_grid = Grid.from_dict(data)
        
        # Verify states are identical
        assert_grid_states_equal(original_grid, restored_grid)
    
    def test_save_load_file(self):
        """Test saving and loading grid to/from file."""
        grid = Grid(2, 2)
        create_block_pattern(grid)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # Save grid
            grid.save_to_file(temp_path)
            
            # Load grid
            loaded_grid = Grid.load_from_file(temp_path)
            
            # Verify states are identical
            assert_grid_states_equal(grid, loaded_grid)
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_load_nonexistent_file_raises_error(self):
        """Test that loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            Grid.load_from_file("nonexistent_file.json")


class TestGridSimulationIntegration:
    """Test grid integration with simulation."""
    
    def test_apply_conway_step(self):
        """Test applying Conway step to grid."""
        grid = Grid(3, 3)
        create_blinker_pattern(grid)
        
        # Store original state
        original_pattern = GridTestHelper.get_pattern_as_list(grid)
        
        # Apply Conway step
        grid.apply_conway_step()
        
        # Verify state changed
        new_pattern = GridTestHelper.get_pattern_as_list(grid)
        assert original_pattern != new_pattern
    
    def test_apply_conway_step_preserves_barriers(self):
        """Test that Conway step preserves orange barriers."""
        grid = Grid(3, 3)
        create_barrier_pattern(grid)
        
        # Apply Conway step
        grid.apply_conway_step()
        
        # Orange barriers should remain
        assert grid.get_cell(1, 1).is_orange()
        assert grid.get_cell(1, 3).is_orange()
        assert grid.get_cell(3, 1).is_orange()
        assert grid.get_cell(3, 3).is_orange()


class TestGridEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_grid_with_single_cell(self):
        """Test operations on single cell grid."""
        grid = Grid(1, 1)
        
        # Basic operations should work
        grid.cycle_cell_color(0, 0)
        assert grid.get_cell(0, 0).is_orange()
        
        grid.clear_all()
        assert grid.get_cell(0, 0).is_black()
        
        # Conway step should work (cell will die due to isolation)
        grid.cycle_cell_color(0, 0)
        grid.cycle_cell_color(0, 0)  # Make it blue
        grid.apply_conway_step()
        assert grid.get_cell(0, 0).is_black()  # Should die
    
    def test_grid_with_single_row(self):
        """Test operations on single row grid."""
        grid = Grid(5, 1)
        
        # Set pattern in single row
        grid.cycle_cell_color(1, 0)  # orange
        grid.cycle_cell_color(2, 0)  # orange
        grid.cycle_cell_color(3, 0)  # orange
        
        # Should be able to apply Conway step
        grid.apply_conway_step()
        
        # Center should survive (has 2 neighbors)
        assert grid.get_cell(2, 0).is_blue_traffic()
    
    def test_grid_with_single_column(self):
        """Test operations on single column grid."""
        grid = Grid(1, 5)
        
        # Set pattern in single column
        grid.cycle_cell_color(0, 1)  # orange
        grid.cycle_cell_color(0, 2)  # orange
        grid.cycle_cell_color(0, 3)  # orange
        
        # Should be able to apply Conway step
        grid.apply_conway_step()
        
        # Center should survive (has 2 neighbors)
        assert grid.get_cell(0, 2).is_blue_traffic()
    
    def test_large_grid_operations(self):
        """Test operations on large grid."""
        grid = Grid(50, 50)
        
        # Should be able to perform basic operations
        grid.cycle_cell_color(25, 25)  # Center
        assert grid.get_cell(25, 25).is_orange()
        
        # Should be able to clear all
        grid.clear_all()
        assert grid.count_active_cells() == 0
        
        # Should be able to apply Conway step
        grid.apply_conway_step()
        assert grid.count_active_cells() == 0  # Should remain empty


class TestGridRepresentation:
    """Test grid string representation."""
    
    def test_grid_repr(self):
        """Test grid string representation."""
        grid = Grid(2, 2)
        
        repr_str = repr(grid)
        assert "Grid(2x2" in repr_str
        assert "0 active cells" in repr_str
        
        # Add some active cells
        grid.cycle_cell_color(0, 0)
        grid.cycle_cell_color(1, 1)
        
        repr_str = repr(grid)
        assert "2 active cells" in repr_str
