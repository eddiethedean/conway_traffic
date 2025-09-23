# Interactive Grid Streamlit App

A bare bones Streamlit app with an interactive grid that you can click on to toggle cell colors.

## Features

- Interactive grid with clickable cells
- Toggle cells between blue and black colors
- User-configurable grid size (1-50 x 1-50)
- Clear all cells functionality
- Random pattern generation
- Grid state visualization

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## How to Use

1. Adjust the grid size using the width and height controls
2. Click on any cell to toggle it between blue (🔵) and black (⚫)
3. Use the "Clear All" button to reset all cells to black
4. Use the "Random Pattern" button to generate a random pattern
5. The "Blue Cells" metric shows how many cells are currently blue

## Project Structure

- `cell.py` - Cell class representing individual grid cells
- `grid.py` - Grid class managing the grid state
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies

