# Interactive Grid App

A web-based interactive grid application built with NiceGUI, featuring clickable cells that toggle between blue and black colors.

## Features

- **Interactive Grid**: Click on cells to toggle between blue and black
- **Perfect Spacing**: Zero gaps between cells using CSS Grid
- **Dynamic Resizing**: Change grid dimensions in real-time
- **Clear All**: Reset all cells to black
- **Blue Cell Counter**: Live count of blue cells
- **Responsive Design**: Works on desktop and mobile

## Technology Stack

- **Frontend**: NiceGUI (Python web framework)
- **Backend**: Python with custom Grid and Cell classes
- **Styling**: CSS Grid for perfect cell spacing
- **Testing**: Pytest for comprehensive test coverage

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd conway_traffic
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Local Development
Run the application locally:
```bash
python app.py
```

The app will be available at `http://localhost:8080`

### Features
- **Click cells** to toggle between blue and black
- **Resize grid** using the width/height controls
- **Clear all** cells with the "Clear All" button
- **View blue cell count** in real-time

## Project Structure

```
conway_traffic/
├── app.py                 # Main NiceGUI application
├── cell.py               # Cell class definition
├── grid.py               # Grid class with cell management
├── requirements.txt      # Python dependencies
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_all.py       # Comprehensive tests
└── README.md            # This file
```

## Core Classes

### Cell Class
- Represents individual grid cells
- Properties: `x`, `y`, `is_blue`
- Methods: `toggle()` to change color state

### Grid Class
- Manages collection of Cell objects
- Properties: `width`, `height`, `cells`
- Methods: `get_cell()`, `toggle_cell()`, `resize()`

### InteractiveGridApp Class
- NiceGUI application controller
- Handles UI rendering and user interactions
- Manages grid state and display updates

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

### Test Coverage
- **Cell functionality**: Initialization, toggling, multiple toggles
- **Grid operations**: Creation, cell access, resizing, toggling
- **App integration**: UI interactions, state management, event handling

## Deployment

### Railway (Recommended)
1. Push code to GitHub
2. Connect repository to Railway
3. Railway auto-detects Python and deploys
4. Access your app at the provided Railway URL

### Other Platforms
- **Render**: Connect GitHub repo, select Python service
- **PythonAnywhere**: Upload files directly
- **Heroku**: Use Procfile for web process

## Development

### Adding Features
1. Modify the Grid or Cell classes for new functionality
2. Update the UI in `app.py` to reflect changes
3. Add tests for new features
4. Update documentation

### Programmatic Grid Control
```python
# Example: Programmatically change grid
app = InteractiveGridApp()
app.grid.toggle_cell(5, 3)  # Toggle cell at (5,3)
app.grid.resize(15, 15)     # Resize to 15x15
app.create_grid()           # Update UI
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Conway's Game of Life simulation
- Pattern saving and loading
- Animation controls
- Grid export/import
- Custom color themes
- Keyboard shortcuts