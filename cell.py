class Cell:
    """Represents a single cell in the grid."""
    
    def __init__(self, x: int, y: int, is_blue: bool = False):
        self.x = x
        self.y = y
        self.is_blue = is_blue
    
    def toggle(self):
        """Toggle the cell's color between blue and black."""
        self.is_blue = not self.is_blue
    
    def set_blue(self):
        """Set the cell to blue."""
        self.is_blue = True
    
    def set_black(self):
        """Set the cell to black."""
        self.is_blue = False
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y}, blue={self.is_blue})"

