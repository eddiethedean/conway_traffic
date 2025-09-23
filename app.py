from nicegui import ui
from grid import Grid

# Global grid state
grid_state = Grid(10, 10)

def create_grid_ui():
    """Create the interactive grid UI"""
    ui.label('Interactive Grid')
    
    # Grid controls
    with ui.row():
        width_input = ui.number('Width', value=10, min=1, max=50)
        height_input = ui.number('Height', value=10, min=1, max=50)
        
        def resize_handler():
            resize_grid(width_input.value, height_input.value, grid_container)
        
        width_input.on('change', resize_handler)
        height_input.on('change', resize_handler)
    
    # Grid display
    grid_container = ui.column()
    create_grid_display(grid_container)

def create_grid_display(container):
    """Create the actual grid display"""
    container.clear()
    
    with container:
        # Add CSS styles
        ui.add_head_html(f"""
        <style>
        .grid-container {{
            display: grid;
            grid-template-columns: repeat({grid_state.width}, 40px);
            grid-template-rows: repeat({grid_state.height}, 40px);
            gap: 0px;
            border: 2px solid #333;
            width: fit-content;
        }}
        .grid-cell {{
            width: 40px;
            height: 40px;
            border: 1px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background-color: white;
            user-select: none;
            transition: background-color 0.1s;
        }}
        .grid-cell:hover {{
            background-color: #f0f0f0;
        }}
        .grid-cell.blue {{
            background-color: #2196F3;
        }}
        .grid-cell.black {{
            background-color: #333;
        }}
        </style>
        """)
        
        # Create grid HTML
        grid_html = '<div class="grid-container">'
        for y in range(grid_state.height):
            for x in range(grid_state.width):
                cell = grid_state.get_cell(x, y)
                cell_class = 'blue' if cell.is_blue else 'black'
                grid_html += f'<div class="grid-cell {cell_class}" onclick="toggleCell({x}, {y})"></div>'
        grid_html += '</div>'
        
        ui.html(grid_html)
        
        # JavaScript for clicks
        ui.add_head_html("""
        <script>
        function toggleCell(x, y) {
            fetch('/api/toggle_cell', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({x: x, y: y})
            }).then(() => location.reload());
        }
        </script>
        """)

def resize_grid(width, height, container=None):
    """Resize the grid"""
    global grid_state
    grid_state.resize(int(width), int(height))
    if container:
        container.clear()
        create_grid_display(container)

# API endpoint for cell toggles
@ui.page('/api/toggle_cell')
def toggle_cell(data: dict):
    """API endpoint to toggle a cell"""
    x, y = data['x'], data['y']
    grid_state.toggle_cell(x, y)
    return {'status': 'success'}

# Create the main page
@ui.page('/')
def main_page():
    create_grid_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=8080)
