class Cell:
    def __init__(self, x, y, is_blue=False):
        self.x = x
        self.y = y
        self.is_blue = is_blue
    
    def toggle(self):
        self.is_blue = not self.is_blue
