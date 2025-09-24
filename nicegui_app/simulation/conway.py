"""Conway's Game of Life simulation for traffic modeling."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.grid import Grid


def run_conway_step(grid: "Grid") -> "Grid":
    """Run one step of Conway's Game of Life simulation adapted for traffic.

    Rules:
    - Orange cells (barriers) remain static and don't evolve
    - Blue cells (traffic) follow Conway's rules:
      * Survive if they have 2-3 traffic neighbors
      * Die if they have <2 or >3 traffic neighbors
    - Empty cells (black) become traffic if they have exactly 3 traffic neighbors

    Args:
        grid: Current grid state

    Returns:
        New grid with one simulation step applied
    """
    from models.grid import Grid

    width, height = grid.width, grid.height
    new_grid = Grid(width, height)

    for y in range(height):
        for x in range(width):
            current_cell = grid.cells[y][x]

            # Preserve orange barriers - they don't evolve
            if current_cell.is_orange():
                new_grid.cells[y][x].set_color_state(1)  # orange
                continue

            # Count traffic neighbors (blue cells)
            traffic_neighbors = _count_traffic_neighbors(grid, x, y)

            if current_cell.is_blue_traffic():
                # Traffic survives if it has 2-3 traffic neighbors
                if traffic_neighbors in [2, 3]:
                    new_grid.cells[y][x].set_color_state(2)  # blue
                else:
                    new_grid.cells[y][x].set_color_state(0)  # black
            else:
                # Empty cell becomes traffic if it has exactly 3 traffic neighbors
                if traffic_neighbors == 3:
                    new_grid.cells[y][x].set_color_state(2)  # blue
                else:
                    new_grid.cells[y][x].set_color_state(0)  # black

    return new_grid


def _count_traffic_neighbors(grid: "Grid", x: int, y: int) -> int:
    """Count the number of traffic (blue) neighbors around a cell.

    Args:
        grid: The grid to check
        x: X coordinate of the cell
        y: Y coordinate of the cell

    Returns:
        Number of traffic neighbors (0-8)
    """
    traffic_count = 0

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the cell itself

            nx, ny = x + dx, y + dy

            # Check bounds
            if 0 <= nx < grid.width and 0 <= ny < grid.height:
                neighbor = grid.cells[ny][nx]
                if neighbor.is_blue_traffic():
                    traffic_count += 1

    return traffic_count
