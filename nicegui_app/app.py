from functools import partial
from grid_persistence import run_conway_step
from nicegui import ui
import os
from grid_persistence import Grid as PersistentGrid

default_save_path = os.path.join(os.path.dirname(__file__), "saved_grid.json")


from typing import Optional
from nicegui.elements.number import Number
from nicegui.elements.label import Label
from nicegui.elements.column import Column



import threading
import time

class InteractiveGridApp:
    simulation_running: bool = False
    simulation_thread: threading.Thread = None
    run_button: any = None
    def run_simulation_step(self) -> None:
        self.grid = run_conway_step(self.grid)
        self.create_grid()
        self.update_blue_count()

    def run_simulation_continuous(self) -> None:
        if self.simulation_running:
            return
        self.simulation_running = True
        if self.run_button:
            self.run_button.text = 'Stop'
        def loop():
            while self.simulation_running:
                self.grid = run_conway_step(self.grid)
                self.create_grid()
                self.update_blue_count()
                time.sleep(0.2)
        self.simulation_thread = threading.Thread(target=loop, daemon=True)
        self.simulation_thread.start()

    def stop_simulation(self) -> None:
        self.simulation_running = False
        if self.run_button:
            self.run_button.text = 'Run'

    width: int
    height: int
    grid: PersistentGrid
    width_input: Optional[Number]
    height_input: Optional[Number]
    blue_count_label: Optional[Label]
    grid_container: Optional[Column]
    save_path: str

    def __init__(self, width: int = 42, height: int = 25) -> None:
        self.width = width
        self.height = height
        self.grid = PersistentGrid(width, height)
        self.width_input = None
        self.height_input = None
        self.blue_count_label = None
        self.grid_container = None
        self.save_path = default_save_path

    def update_blue_count(self) -> None:
        """Update the blue cell count display"""
        if self.blue_count_label:
            orange_count = sum(
                1 for row in self.grid.cells for cell in row if cell.is_blue
            )
            self.blue_count_label.text = f"Orange cells: {orange_count}"

    def on_cell_click(self, x: int, y: int) -> None:
        """Cycle cell color: black -> orange -> blue -> black"""
        cell = self.grid.get_cell(x, y)
        # color_state: 0=black, 1=orange, 2=blue
        prev_state = getattr(cell, 'color_state', None)
        if prev_state is None:
            cell.color_state = 1  # Always start with orange on first click
        else:
            cell.color_state = (cell.color_state + 1) % 3
        if cell.color_state == 0:
            cell.is_blue = False
        elif cell.color_state == 1:
            cell.is_blue = True
        elif cell.color_state == 2:
            cell.is_blue = True
        self.create_grid()
        self.update_blue_count()

    def resize_grid(self) -> None:
        """Resize the grid based on input values"""
        try:
            new_width = int(self.width_input.value)
            new_height = int(self.height_input.value)

            if new_width > 0 and new_height > 0:
                self.grid.resize(new_width, new_height)
                self.create_grid()
            else:
                pass  # Invalid input, do nothing
        except ValueError:
            pass  # Invalid input, do nothing

    def clear_all(self) -> None:
        """Clear all cells"""
        for row in self.grid.cells:
            for cell in row:
                cell.is_blue = False
                if hasattr(cell, 'color_state'):
                    cell.color_state = 0
        self.create_grid()
        self.update_blue_count()

    def save_grid(self) -> None:
        self.grid.save_to_file(self.save_path)
        ui.notify(f"Grid saved to {self.save_path}")

    def load_grid(self) -> None:
        if os.path.exists(self.save_path):
            loaded_grid = PersistentGrid.load_from_file(self.save_path)
            self.grid = loaded_grid
            self.width = loaded_grid.width
            self.height = loaded_grid.height
            if self.width_input:
                self.width_input.value = self.width
            if self.height_input:
                self.height_input.value = self.height
            self.create_grid()
            self.update_blue_count()
            ui.notify(f"Grid loaded from {self.save_path}")
        else:
            ui.notify(f"No saved grid found at {self.save_path}", color="negative")

    def create_grid(self) -> None:
        """Create the grid display"""
        if self.grid_container:
            self.grid_container.clear()

            with self.grid_container:
                # Create CSS for perfect grid
                ui.add_head_html(
                    """
                <style>
                .grid-container {
                    display: grid;
                    gap: 0px;
                    margin: 20px 0;
                }
                .grid-cell {
                    width: 40px;
                    height: 40px;
                    border: 1px solid #ccc;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    color: white;
                    transition: background-color 0.2s;
                }
                .grid-cell.orange {
                    background-color: orange;
                }
                .grid-cell.blue {
                    background-color: #2196F3;
                }
                .grid-cell.black {
                    background-color: #333333;
                }
                .grid-cell:hover {
                    opacity: 0.8;
                }
                </style>
                """
                )

                # Create grid container
                grid_style = f"grid-template-columns: repeat({self.grid.width}, 40px);"
                with ui.column().classes("grid-container").style(grid_style):
                    for y in range(self.grid.height):
                        for x in range(self.grid.width):
                            cell = self.grid.get_cell(x, y)
                            color_state = getattr(cell, 'color_state', 1 if cell.is_blue else 0)
                            if color_state == 2:
                                color_class = "blue"
                            elif color_state == 1:
                                color_class = "orange"
                            else:
                                color_class = "black"

                            # Create clickable cell
                            cell_div = ui.html(
                                f'<div class="grid-cell {color_class}"></div>'
                            )
                            cell_div.on(
                                "click", partial(self.on_cell_click, x, y)
                            )


    def create_ui(self) -> None:
        """Create the user interface"""
        ui.page_title("Interactive Grid")

        # Header
        ui.html("<h1>Interactive Grid</h1>")
        ui.html("<p>Click on cells to toggle between orange and black</p>")

        # Controls
        with ui.row().classes('w-full gap-4 items-end'):
            self.width_input = ui.number('Width', value=self.width, min=1, max=1000)
            self.height_input = ui.number('Height', value=self.height, min=1, max=1000)
            ui.button('Resize Grid', on_click=self.resize_grid)
            ui.button('Clear All', on_click=self.clear_all)
            ui.button('Save Grid', on_click=self.save_grid)
            ui.button('Load Grid', on_click=self.load_grid)
            self.run_button = ui.button('Run', on_click=self.toggle_simulation)

        # Grid info
        with ui.row().classes("w-full gap-4"):
            ui.html(f"<p>Grid size: {self.grid.width} x {self.grid.height}</p>")
            self.blue_count_label = ui.label("Orange cells: 0")

        # Create grid container
        self.grid_container = ui.column()

        # Create the grid
        self.create_grid()

        # Update blue count
        self.update_blue_count()

    def toggle_simulation(self) -> None:
        if not self.simulation_running:
            self.run_simulation_continuous()
        else:
            self.stop_simulation()


@ui.page("/")
def main_page() -> InteractiveGridApp:
    app = InteractiveGridApp()
    app.create_ui()
    return app


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8081)
