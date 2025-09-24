def run_conway_step(grid: "Grid") -> "Grid":
    width, height = grid.width, grid.height
    new_grid = Grid(width, height)
    for y in range(height):
        for x in range(width):
            cell = grid.cells[y][x]
            # Preserve orange cells
            if hasattr(cell, 'color_state') and cell.color_state == 1:
                new_grid.cells[y][x].color_state = 1
                new_grid.cells[y][x].is_blue = True
                continue
            live_neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        neighbor = grid.cells[ny][nx]
                        if hasattr(neighbor, 'color_state') and neighbor.color_state == 2:
                            live_neighbors += 1
            if hasattr(cell, 'color_state') and cell.color_state == 2:
                new_grid.cells[y][x].color_state = 2 if live_neighbors in [2, 3] else 0
                new_grid.cells[y][x].is_blue = live_neighbors in [2, 3]
            else:
                new_grid.cells[y][x].color_state = 2 if live_neighbors == 3 else 0
                new_grid.cells[y][x].is_blue = live_neighbors == 3
    return new_grid
import json
from cell import Cell

from typing import List, Dict, Any, ClassVar


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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "cells": [
                [
                    {
                        "is_blue": cell.is_blue,
                        "color_state": getattr(cell, "color_state", 1 if cell.is_blue else 0)
                    }
                    for cell in row
                ]
                for row in self.cells
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Grid":
        grid = cls(data["width"], data["height"])
        for y, row in enumerate(data["cells"]):
            for x, cell_data in enumerate(row):
                if isinstance(cell_data, dict):
                    grid.cells[y][x].is_blue = cell_data.get("is_blue", False)
                    grid.cells[y][x].color_state = cell_data.get("color_state", 1 if cell_data.get("is_blue", False) else 0)
                else:
                    # Backward compatibility: old format was just is_blue
                    grid.cells[y][x].is_blue = cell_data
                    grid.cells[y][x].color_state = 1 if cell_data else 0
        return grid

    def save_to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load_from_file(cls, filename: str) -> "Grid":
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)
