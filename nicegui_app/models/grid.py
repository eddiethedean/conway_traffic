"""Grid class for Conway Traffic simulation."""

import json
from typing import List, Dict, Any, Optional, TYPE_CHECKING

from .cell import Cell

if TYPE_CHECKING:
    from simulation.conway import run_conway_step


class Grid:
    """Grid class that manages a 2D array of cells for traffic simulation.

    Features:
    - Cell management and access
    - Grid resizing
    - Conway's Game of Life simulation
    - Save/load functionality
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a grid with the specified dimensions.

        Args:
            width: Number of columns
            height: Number of rows
            
        Raises:
            ValueError: If dimensions are not positive
        """
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []
        self._initialize_cells()

    def _initialize_cells(self) -> None:
        """Initialize the 2D array of cells."""
        self.cells = []
        for y in range(self.height):
            row: List[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at the specified coordinates.

        Args:
            x: X coordinate (column)
            y: Y coordinate (row)

        Returns:
            The cell at the specified coordinates

        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(
                f"Cell coordinates ({x}, {y}) out of bounds for grid {self.width}x{self.height}"
            )
        return self.cells[y][x]

    def toggle_cell(self, x: int, y: int) -> None:
        """Toggle a cell's state using the old boolean method.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.cells[y][x].toggle()

    def cycle_cell_color(self, x: int, y: int) -> None:
        """Cycle a cell's color state: black -> orange -> blue -> black.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.get_cell(x, y).cycle_color()

    def resize(self, new_width: int, new_height: int) -> None:
        """Resize the grid to new dimensions.

        Args:
            new_width: New number of columns
            new_height: New number of rows
        """
        if new_width <= 0 or new_height <= 0:
            raise ValueError("Grid dimensions must be positive")

        # Create new cells
        new_cells = []
        for y in range(new_height):
            row = []
            for x in range(new_width):
                # Preserve existing cells if possible
                if y < self.height and x < self.width:
                    row.append(self.cells[y][x])
                else:
                    row.append(Cell(x, y))
            new_cells.append(row)

        self.width = new_width
        self.height = new_height
        self.cells = new_cells

    def clear_all(self) -> None:
        """Reset all cells to black (empty road) state."""
        for row in self.cells:
            for cell in row:
                cell.reset()

    def count_active_cells(self) -> int:
        """Count the number of active cells (orange + blue).

        Returns:
            Number of active cells
        """
        return sum(1 for row in self.cells for cell in row if cell.is_blue)

    def count_orange_cells(self) -> int:
        """Count the number of orange cells (barriers).

        Returns:
            Number of orange cells
        """
        return sum(1 for row in self.cells for cell in row if cell.is_orange())

    def count_blue_cells(self) -> int:
        """Count the number of blue cells (traffic).

        Returns:
            Number of blue cells
        """
        return sum(1 for row in self.cells for cell in row if cell.is_blue_traffic())

    def apply_conway_step(self) -> None:
        """Apply one step of Conway's Game of Life simulation to this grid."""
        from simulation.conway import run_conway_step

        new_grid = run_conway_step(self)
        self.cells = new_grid.cells

    def to_dict(self) -> Dict[str, Any]:
        """Convert the grid to a dictionary for serialization.

        Returns:
            Dictionary representation of the grid
        """
        return {
            "width": self.width,
            "height": self.height,
            "cells": [
                [
                    {"is_blue": cell.is_blue, "color_state": cell.color_state}
                    for cell in row
                ]
                for row in self.cells
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Grid":
        """Create a grid from a dictionary representation.

        Args:
            data: Dictionary containing grid data

        Returns:
            New Grid instance
        """
        grid = cls(data["width"], data["height"])

        for y, row in enumerate(data["cells"]):
            for x, cell_data in enumerate(row):
                if isinstance(cell_data, dict):
                    # New format with color_state
                    grid.cells[y][x].is_blue = cell_data.get("is_blue", False)
                    grid.cells[y][x].color_state = cell_data.get(
                        "color_state", 1 if cell_data.get("is_blue", False) else 0
                    )
                else:
                    # Backward compatibility: old format was just is_blue boolean
                    grid.cells[y][x].is_blue = cell_data
                    grid.cells[y][x].color_state = 1 if cell_data else 0

        return grid

    def save_to_file(self, filename: str) -> None:
        """Save the grid to a JSON file.

        Args:
            filename: Path to the file to save to
        """
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load_from_file(cls, filename: str) -> "Grid":
        """Load a grid from a JSON file.

        Args:
            filename: Path to the file to load from

        Returns:
            New Grid instance loaded from file
        """
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        """Return string representation of the grid."""
        return f"Grid({self.width}x{self.height}, {self.count_active_cells()} active cells)"
