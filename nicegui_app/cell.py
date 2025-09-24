class Cell:
    x: int
    y: int
    is_blue: bool

    def __init__(self, x: int, y: int, is_blue: bool = False) -> None:
        self.x = x
        self.y = y
        self.is_blue = is_blue
    # self.color_state = 0  # 0=black, 1=orange, 2=blue

    def toggle(self) -> None:
        self.is_blue = not self.is_blue
