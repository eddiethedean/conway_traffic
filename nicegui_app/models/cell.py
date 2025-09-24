"""Cell class for Conway Traffic simulation."""

from typing import Optional


class Cell:
    """Represents a single cell in the traffic simulation grid.

    Each cell can be in one of three states:
    - 0: Black (empty road)
    - 1: Orange (traffic barrier/obstacle)
    - 2: Blue (moving traffic)
    """

    def __init__(
        self, x: int, y: int, color_state: int = 0, is_blue: Optional[bool] = None
    ) -> None:
        """Initialize a cell at the given coordinates.

        Args:
            x: X coordinate in the grid
            y: Y coordinate in the grid
            color_state: Initial color state (0=black, 1=orange, 2=blue)
            is_blue: Legacy parameter for backward compatibility
        """
        self.x = x
        self.y = y

        # Handle legacy is_blue parameter
        if is_blue is not None:
            self.color_state = 1 if is_blue else 0
        else:
            self.color_state = color_state

    @property
    def is_blue(self) -> bool:
        """Return True if cell is active (orange or blue).

        This property maintains backward compatibility with existing code
        that expects a boolean is_blue attribute.
        """
        return self.color_state in [1, 2]

    @is_blue.setter
    def is_blue(self, value: bool) -> None:
        """Set the cell state based on boolean value.

        Args:
            value: True sets to orange (1), False sets to black (0)
        """
        self.color_state = 1 if value else 0

    def cycle_color(self) -> None:
        """Cycle through color states: black -> orange -> blue -> black."""
        self.color_state = (self.color_state + 1) % 3

    def reset(self) -> None:
        """Reset cell to black (empty) state."""
        self.color_state = 0

    def set_color_state(self, state: int) -> None:
        """Set the color state directly.

        Args:
            state: 0=black, 1=orange, 2=blue
        """
        if state not in [0, 1, 2]:
            raise ValueError("Color state must be 0, 1, or 2")
        self.color_state = state

    def is_black(self) -> bool:
        """Return True if cell is black (empty road)."""
        return self.color_state == 0

    def is_orange(self) -> bool:
        """Return True if cell is orange (traffic barrier)."""
        return self.color_state == 1

    def is_blue_traffic(self) -> bool:
        """Return True if cell is blue (moving traffic)."""
        return self.color_state == 2

    def toggle(self) -> None:
        """Toggle using the old boolean method for backward compatibility."""
        self.is_blue = not self.is_blue

    def __repr__(self) -> str:
        """Return string representation of the cell."""
        state_names = {0: "black", 1: "orange", 2: "blue"}
        return f"Cell({self.x}, {self.y}, {state_names[self.color_state]})"
