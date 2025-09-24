from cell import Cell

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.cells.append(row)
    
    def get_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Cell coordinates out of bounds")
        return self.cells[y][x]
    
    def toggle_cell(self, x, y):
        self.cells[y][x].toggle()
    
    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.cells = []
        for y in range(new_height):
            row = []
            for x in range(new_width):
                row.append(Cell(x, y))
            self.cells.append(row)
