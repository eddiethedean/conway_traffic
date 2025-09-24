"""Conway Traffic Simulation App - Main application."""

import os
import threading
import time
from functools import partial
from typing import Optional

from nicegui import ui
from nicegui.elements.number import Number
from nicegui.elements.label import Label
from nicegui.elements.column import Column

from models import Grid
from simulation import run_conway_step
from ui import GRID_CSS

DEFAULT_SAVE_PATH = os.path.join(os.path.dirname(__file__), "saved_grid.json")


class InteractiveGridApp:
    """Main application class for Conway Traffic simulation."""

    def __init__(self, width: int = 42, height: int = 25) -> None:
        """Initialize the application.

        Args:
            width: Initial grid width
            height: Initial grid height
        """
        self.width = width
        self.height = height
        self.grid = Grid(width, height)
        self.save_path = DEFAULT_SAVE_PATH

        # UI components
        self.width_input: Optional[Number] = None
        self.height_input: Optional[Number] = None
        self.traffic_count_label: Optional[Label] = None
        self.grid_container: Optional[Column] = None
        self.run_button: Optional[ui.button] = None

        # Simulation state
        self.simulation_running: bool = False
        self.simulation_thread: Optional[threading.Thread] = None

    def run_simulation_step(self) -> None:
        """Run a single simulation step."""
        self.grid.apply_conway_step()
        self.create_grid()
        self.update_traffic_count()

    def run_simulation_continuous(self) -> None:
        """Start continuous simulation."""
        if self.simulation_running:
            return

        self.simulation_running = True
        if self.run_button:
            self.run_button.text = "Stop"

        def simulation_loop():
            """Simulation loop running in separate thread."""
            while self.simulation_running:
                self.grid.apply_conway_step()
                self.create_grid()
                self.update_traffic_count()
                time.sleep(0.2)

        self.simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        self.simulation_thread.start()

    def stop_simulation(self) -> None:
        """Stop continuous simulation."""
        self.simulation_running = False
        if self.run_button:
            self.run_button.text = "Run"

    def update_traffic_count(self) -> None:
        """Update the traffic count display."""
        if self.traffic_count_label:
            active_count = self.grid.count_active_cells()
            self.traffic_count_label.text = f"Active traffic elements: {active_count}"

    def on_cell_click(self, x: int, y: int) -> None:
        """Cycle cell color: black -> orange -> blue -> black."""
        self.grid.cycle_cell_color(x, y)
        self.create_grid()
        self.update_traffic_count()

    def resize_grid(self) -> None:
        """Resize the grid based on input values."""
        if self.width_input is None or self.height_input is None:
            return

        try:
            new_width = int(self.width_input.value)
            new_height = int(self.height_input.value)

            if new_width > 0 and new_height > 0:
                self.grid.resize(new_width, new_height)
                self.width = new_width
                self.height = new_height
                self.create_grid()
        except (ValueError, TypeError):
            # Invalid input, do nothing
            pass

    def clear_all(self) -> None:
        """Clear all cells to black (empty road) state."""
        self.grid.clear_all()
        self.create_grid()
        self.update_traffic_count()

    def save_grid(self) -> None:
        self.grid.save_to_file(self.save_path)
        ui.notify(f"Grid saved to {self.save_path}")

    def load_grid(self) -> None:
        """Load grid from saved file."""
        if os.path.exists(self.save_path):
            self.grid = Grid.load_from_file(self.save_path)
            self.width = self.grid.width
            self.height = self.grid.height

            if self.width_input:
                self.width_input.value = self.width
            if self.height_input:
                self.height_input.value = self.height

            self.create_grid()
            self.update_traffic_count()
            ui.notify(f"Traffic pattern loaded from {self.save_path}")
        else:
            ui.notify(f"No saved pattern found at {self.save_path}", color="negative")

    def create_grid(self) -> None:
        """Create the grid display."""
        if self.grid_container:
            self.grid_container.clear()

            with self.grid_container:
                # Add CSS styles
                ui.add_head_html(GRID_CSS)

                # Create grid container
                grid_style = f"grid-template-columns: repeat({self.grid.width}, 40px);"
                with ui.column().classes("grid-container").style(grid_style):
                    for y in range(self.grid.height):
                        for x in range(self.grid.width):
                            cell = self.grid.get_cell(x, y)

                            # Determine color class based on cell state
                            if cell.is_blue_traffic():
                                color_class = "blue"
                            elif cell.is_orange():
                                color_class = "orange"
                            else:
                                color_class = "black"

                            # Create clickable cell
                            cell_div = ui.html(
                                f'<div class="grid-cell {color_class}"></div>'
                            )
                            cell_div.on("click", partial(self.on_cell_click, x, y))

    def create_ui(self) -> None:
        """Create the user interface."""
        ui.page_title("Conway Traffic Simulation")

        # Header
        ui.html("<h1>🚗 Conway Traffic Simulation</h1>")
        ui.html(
            "<p>Click cells to cycle: Empty Road (black) → Traffic Barrier (orange) → Moving Traffic (blue)</p>"
        )

        # Controls
        with ui.row().classes("w-full gap-4 items-end"):
            self.width_input = ui.number("Width", value=self.width, min=1, max=1000)
            self.height_input = ui.number("Height", value=self.height, min=1, max=1000)
            ui.button("Resize Grid", on_click=self.resize_grid)
            ui.button("Clear All", on_click=self.clear_all)
            ui.button("Save Pattern", on_click=self.save_grid)
            ui.button("Load Pattern", on_click=self.load_grid)
            self.run_button = ui.button(
                "Start Simulation", on_click=self.toggle_simulation
            )

        # Grid info
        with ui.row().classes("w-full gap-4"):
            ui.html(f"<p>Grid size: {self.grid.width} x {self.grid.height}</p>")
            self.traffic_count_label = ui.label("Active traffic elements: 0")

        # Create grid container
        self.grid_container = ui.column()

        # Create the grid
        self.create_grid()

        # Update traffic count
        self.update_traffic_count()

    def toggle_simulation(self) -> None:
        """Toggle simulation on/off."""
        if not self.simulation_running:
            self.run_simulation_continuous()
        else:
            self.stop_simulation()


@ui.page("/")
def main_page() -> InteractiveGridApp:
    """Main page route."""
    app = InteractiveGridApp()
    app.create_ui()
    return app


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8081)
