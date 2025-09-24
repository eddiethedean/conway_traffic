# Conway Traffic Simulation App

A web-based traffic simulation system built with NiceGUI, featuring an interactive grid where you can design traffic patterns and watch them evolve using cellular automata rules.

## Features

- **Interactive Traffic Design**: Click cells to cycle through empty roads (black), barriers (orange), and traffic (blue)
- **Conway's Game of Life Simulation**: Watch traffic evolve according to cellular automata rules
- **Real-time Animation**: Continuous simulation with start/stop controls
- **Perfect Grid Layout**: Zero gaps between cells using CSS Grid
- **Dynamic Resizing**: Change grid dimensions in real-time
- **Save & Load**: Persist your traffic scenarios to JSON files
- **Live Statistics**: Real-time count of active traffic elements
- **Responsive Design**: Works on desktop and mobile

## Technology Stack

- **Frontend**: NiceGUI (Python web framework)
- **Backend**: Python with custom Grid and Cell classes implementing cellular automata
- **Simulation Engine**: Conway's Game of Life rules adapted for traffic modeling
- **Styling**: CSS Grid for perfect cell spacing
- **Testing**: Pytest with comprehensive test coverage including BDD scenarios
- **Persistence**: JSON-based save/load for traffic patterns

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
- **Click cells** to cycle through empty roads (black), barriers (orange), and traffic (blue)
- **Run simulation** to watch traffic evolve according to Conway's rules
- **Resize grid** using the width/height controls
- **Save/Load** traffic patterns to/from JSON files
- **Clear all** cells with the "Clear All" button
- **View traffic count** in real-time

## Project Structure

```
conway_traffic/nicegui_app/
├── app.py                 # Main NiceGUI application with traffic simulation
├── cell.py               # Cell class definition for traffic elements
├── grid.py               # Basic Grid class with cell management
├── grid_persistence.py   # Enhanced Grid with Conway's rules and persistence
├── requirements.txt      # Python dependencies
├── saved_grid.json       # Default saved traffic pattern
├── tests/                # Comprehensive test suite
│   ├── __init__.py
│   ├── test_all.py       # Core functionality tests
│   ├── test_conway_simulation.py  # Conway's rules tests
│   ├── test_grid_persistence.py   # Save/load tests
│   └── ...               # Additional test files
├── features/             # BDD test scenarios
│   ├── app_features.feature
│   ├── run_simulation.feature
│   └── save_load_grid.feature
└── README.md            # This file
```

## Core Classes

### Cell Class
- Represents individual traffic elements (roads, barriers, vehicles)
- Properties: `x`, `y`, `is_blue`, `color_state`
- Methods: `toggle()` to change state

### Grid Class (grid.py)
- Basic grid management with Cell objects
- Properties: `width`, `height`, `cells`
- Methods: `get_cell()`, `toggle_cell()`, `resize()`

### Grid Class (grid_persistence.py)
- Enhanced grid with Conway's Game of Life simulation
- Includes save/load functionality and traffic evolution rules
- Methods: `to_dict()`, `from_dict()`, `save_to_file()`, `load_from_file()`

### InteractiveGridApp Class
- NiceGUI application controller for traffic simulation
- Handles UI rendering, user interactions, and simulation controls
- Manages grid state, continuous simulation, and display updates

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

### Test Coverage
- **Cell functionality**: Initialization, toggling, color state management
- **Grid operations**: Creation, cell access, resizing, Conway's rules simulation
- **App integration**: UI interactions, simulation controls, save/load functionality
- **Conway's Game of Life**: Traffic evolution rules, neighbor counting, state transitions
- **BDD Scenarios**: Feature-based testing with Gherkin syntax

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

### Programmatic Traffic Control
```python
# Example: Programmatically create traffic patterns
app = InteractiveGridApp()
app.grid.get_cell(5, 3).color_state = 2  # Set traffic at (5,3)
app.grid.get_cell(6, 3).color_state = 1  # Set barrier at (6,3)
app.grid.resize(15, 15)                   # Resize to 15x15
app.create_grid()                         # Update UI
app.run_simulation_step()                 # Run one simulation step
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

- **Traffic Patterns**: Pre-defined road layouts (intersections, highways, roundabouts)
- **Speed Controls**: Adjustable simulation speed and step-by-step mode
- **Export Features**: Save patterns as images or animated GIFs
- **Advanced Rules**: Different traffic behaviors (pedestrians, emergency vehicles)
- **Statistics**: Traffic flow metrics and congestion analysis
- **Custom Themes**: Different color schemes and visual styles
- **Keyboard Shortcuts**: Hotkeys for common operations