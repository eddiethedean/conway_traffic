from typing import List
from cell import Cell


class Grid:
    """Manages a grid of cells with X by Y dimensions."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = []
        self._initialize_grid()
    
    def _initialize_grid(self):
        """Initialize the grid with empty cells."""
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y, is_blue=False))
            self.cells.append(row)
    
    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at the specified coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None
    
    def toggle_cell(self, x: int, y: int):
        """Toggle a cell's color at the specified coordinates."""
        cell = self.get_cell(x, y)
        if cell:
            cell.toggle()
    
    def resize(self, new_width: int, new_height: int):
        """Resize the grid to new dimensions."""
        self.width = new_width
        self.height = new_height
        self._initialize_grid()
    
    def get_blue_cells(self) -> List[Cell]:
        """Get all blue cells in the grid."""
        blue_cells = []
        for row in self.cells:
            for cell in row:
                if cell.is_blue:
                    blue_cells.append(cell)
        return blue_cells
    
    def clear_all(self):
        """Clear all cells (set to black)."""
        for row in self.cells:
            for cell in row:
                cell.set_black()
    
    def __repr__(self):
        return f"Grid({self.width}x{self.height})"

