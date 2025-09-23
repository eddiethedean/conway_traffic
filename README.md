# Interactive Grid App

A simple NiceGUI app with an interactive grid that you can click on to toggle cell colors.

## Features

- Interactive grid with clickable cells
- Toggle cells between blue and black colors
- User-configurable grid size (1-50 x 1-50)
- Real-time grid resizing
- Clean, minimal interface

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the NiceGUI app:
```bash
python app.py
```

The app will start on `http://localhost:8080`

## How to Use

1. Adjust the grid size using the width and height number inputs
2. Click on any cell to toggle it between blue and black
3. The grid resizes automatically as you change the dimensions
4. All data is cleared when you resize the grid

## Project Structure

- `cell.py` - Cell class representing individual grid cells
- `grid.py` - Grid class managing the grid state
- `app.py` - Main NiceGUI application
- `tests/` - Unit tests for the grid functionality
- `requirements.txt` - Python dependencies

## Testing

Run the tests:
```bash
cd tests
python -m pytest test_grid.py -v
```

