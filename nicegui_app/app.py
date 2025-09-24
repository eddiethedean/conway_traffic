from nicegui import ui
from nicegui_app.grid import Grid


class InteractiveGridApp:
    def __init__(self):
        self.grid = Grid(10, 10)
        self.width_input = None
        self.height_input = None
        self.blue_count_label = None
        self.grid_container = None
        
    def update_blue_count(self):
        """Update the blue cell count display"""
        if self.blue_count_label:
            blue_count = sum(1 for row in self.grid.cells for cell in row if cell.is_blue)
            self.blue_count_label.text = f"Blue cells: {blue_count}"
    
    def on_cell_click(self, x, y):
        """Handle cell click events"""
        # Toggle the cell
        self.grid.toggle_cell(x, y)
        
        # Update the grid display
        self.create_grid()
        
        # Update blue count
        self.update_blue_count()
    
    def resize_grid(self):
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
    
    def clear_all(self):
        """Clear all cells"""
        for row in self.grid.cells:
            for cell in row:
                cell.is_blue = False
        self.create_grid()
        self.update_blue_count()
    
    def create_grid(self):
        """Create the grid display"""
        if self.grid_container:
            self.grid_container.clear()
            
            with self.grid_container:
                # Create CSS for perfect grid
                ui.add_head_html('''
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
                ''')
                
                # Create grid container
                grid_style = f"grid-template-columns: repeat({self.grid.width}, 40px);"
                with ui.column().classes('grid-container').style(grid_style):
                    for y in range(self.grid.height):
                        for x in range(self.grid.width):
                            cell = self.grid.get_cell(x, y)
                            color_class = "blue" if cell.is_blue else "black"
                            
                            # Create clickable cell
                            cell_div = ui.html(f'<div class="grid-cell {color_class}"></div>')
                            cell_div.on('click', lambda x=x, y=y: self.on_cell_click(x, y))
    
    def create_ui(self):
        """Create the user interface"""
        ui.page_title('Interactive Grid')
        
        # Header
        ui.html('<h1>Interactive Grid</h1>')
        ui.html('<p>Click on cells to toggle between blue and black</p>')
        
        # Controls
        with ui.row().classes('w-full gap-4 items-end'):
            self.width_input = ui.number('Width', value=10, min=1, max=50)
            self.height_input = ui.number('Height', value=10, min=1, max=50)
            ui.button('Resize Grid', on_click=self.resize_grid)
            ui.button('Clear All', on_click=self.clear_all)
        
        # Grid info
        with ui.row().classes('w-full gap-4'):
            ui.html(f'<p>Grid size: {self.grid.width} x {self.grid.height}</p>')
            self.blue_count_label = ui.label('Blue cells: 0')
        
        # Create grid container
        self.grid_container = ui.column()
        
        # Create the grid
        self.create_grid()
        
        # Update blue count
        self.update_blue_count()


def main():
    """Main function to run the app"""
    app = InteractiveGridApp()
    app.create_ui()
    ui.run(port=8080, title='Interactive Grid')


if __name__ in {"__main__", "__mp_main__"}:
    main()