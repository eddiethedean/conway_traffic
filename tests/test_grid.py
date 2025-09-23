import pytest
from grid import Grid

def test_grid_creation():
    """Test basic grid creation"""
    grid = Grid(5, 5)
    assert grid.width == 5
    assert grid.height == 5

def test_cell_operations():
    """Test setting cells to blue"""
    grid = Grid(3, 3)
    grid.get_cell(0, 0).set_blue()
    assert grid.get_cell(0, 0).is_blue == True
    assert grid.get_cell(1, 1).is_blue == False

def test_resize_clears_data():
    """Test that resize clears all data"""
    grid = Grid(3, 3)
    grid.get_cell(0, 0).set_blue()
    grid.get_cell(1, 1).set_blue()
    
    grid.resize(2, 2)
    assert grid.get_cell(0, 0).is_blue == False
    assert grid.get_cell(1, 1).is_blue == False
    assert len(grid.get_blue_cells()) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])