from cell import Cell

from typing import List


class Grid:
    width: int
    height: int
    cells: List[List[Cell]]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []
        for y in range(height):
            row: List[Cell] = []
            for x in range(width):
                row.append(Cell(x, y))
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Cell coordinates out of bounds")
        return self.cells[y][x]

    def toggle_cell(self, x: int, y: int) -> None:
        self.cells[y][x].toggle()

    def resize(self, new_width: int, new_height: int) -> None:
        self.width = new_width
        self.height = new_height
        self.cells = []
        for y in range(new_height):
            row: List[Cell] = []
            for x in range(new_width):
                row.append(Cell(x, y))
            self.cells.append(row)
