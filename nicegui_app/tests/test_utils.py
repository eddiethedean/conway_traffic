"""Test utilities and fixtures for Conway Traffic simulation tests."""

import pytest
import tempfile
import os
from typing import Generator, Tuple
from models import Cell, Grid
from app import InteractiveGridApp


@pytest.fixture
def sample_cell() -> Cell:
    """Create a sample cell for testing."""
    return Cell(5, 10)


@pytest.fixture
def sample_grid() -> Grid:
    """Create a sample grid for testing."""
    return Grid(5, 5)


@pytest.fixture
def sample_app() -> InteractiveGridApp:
    """Create a sample app instance for testing."""
    return InteractiveGridApp(width=5, height=5)


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create a temporary file for testing file operations."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def create_blinker_pattern(grid: Grid) -> None:
    """Create a blinker pattern (horizontal line of 3 blue cells)."""
    if grid.width >= 3 and grid.height >= 3:
        grid.cells[1][0].set_color_state(2)  # blue
        grid.cells[1][1].set_color_state(2)  # blue
        grid.cells[1][2].set_color_state(2)  # blue


def create_block_pattern(grid: Grid) -> None:
    """Create a block pattern (2x2 square of blue cells)."""
    if grid.width >= 2 and grid.height >= 2:
        grid.cells[0][0].set_color_state(2)  # blue
        grid.cells[0][1].set_color_state(2)  # blue
        grid.cells[1][0].set_color_state(2)  # blue
        grid.cells[1][1].set_color_state(2)  # blue


def create_barrier_pattern(grid: Grid) -> None:
    """Create a pattern with orange barriers and blue traffic."""
    if grid.width >= 3 and grid.height >= 3:
        # Orange barriers (static)
        grid.cells[1][1].set_color_state(1)  # orange
        grid.cells[1][2].set_color_state(1)  # orange
        grid.cells[2][1].set_color_state(1)  # orange
        grid.cells[2][2].set_color_state(1)  # orange
        
        # Blue traffic (evolves)
        grid.cells[1][0].set_color_state(2)  # blue


def assert_grid_states_equal(grid1: Grid, grid2: Grid) -> None:
    """Assert that two grids have the same state."""
    assert grid1.width == grid2.width
    assert grid1.height == grid2.height
    
    for y in range(grid1.height):
        for x in range(grid1.width):
            cell1 = grid1.cells[y][x]
            cell2 = grid2.cells[y][x]
            assert cell1.color_state == cell2.color_state, f"Cell ({x}, {y}) states differ: {cell1.color_state} vs {cell2.color_state}"


def count_cells_by_state(grid: Grid) -> Tuple[int, int, int]:
    """Count cells by their state: (black, orange, blue)."""
    black_count = orange_count = blue_count = 0
    
    for row in grid.cells:
        for cell in row:
            if cell.is_black():
                black_count += 1
            elif cell.is_orange():
                orange_count += 1
            elif cell.is_blue_traffic():
                blue_count += 1
    
    return black_count, orange_count, blue_count


class GridTestHelper:
    """Helper class for complex grid testing scenarios."""
    
    @staticmethod
    def create_custom_pattern(grid: Grid, pattern: list) -> None:
        """Create a custom pattern from a list of (x, y, state) tuples."""
        for x, y, state in pattern:
            if 0 <= x < grid.width and 0 <= y < grid.height:
                grid.cells[y][x].set_color_state(state)
    
    @staticmethod
    def get_pattern_as_list(grid: Grid) -> list:
        """Get the current grid pattern as a list of (x, y, state) tuples."""
        pattern = []
        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.cells[y][x]
                if cell.color_state != 0:  # Only non-black cells
                    pattern.append((x, y, cell.color_state))
        return pattern
    
    @staticmethod
    def simulate_steps(grid: Grid, steps: int) -> Grid:
        """Simulate multiple Conway steps and return the final grid."""
        from simulation import run_conway_step
        
        current_grid = grid
        for _ in range(steps):
            current_grid = run_conway_step(current_grid)
        return current_grid
