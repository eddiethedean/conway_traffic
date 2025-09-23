import streamlit as st
import pandas as pd
from grid import Grid

# Initialize session state
if 'grid' not in st.session_state:
    st.session_state.grid = Grid(10, 10)

def main():
    st.title("Interactive Grid")
    st.write("Click on cells to toggle between blue and black colors")
    
    # Grid size controls
    col1, col2 = st.columns(2)
    
    with col1:
        width = st.number_input("Grid Width", min_value=1, max_value=50, value=st.session_state.grid.width)
    
    with col2:
        height = st.number_input("Grid Height", min_value=1, max_value=50, value=st.session_state.grid.height)
    
    # Resize grid if dimensions changed
    if width != st.session_state.grid.width or height != st.session_state.grid.height:
        st.session_state.grid.resize(width, height)
        st.rerun()
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Clear All"):
            st.session_state.grid.clear_all()
            st.rerun()
    
    with col2:
        if st.button("Random Pattern"):
            import random
            for row in st.session_state.grid.cells:
                for cell in row:
                    cell.is_blue = random.choice([True, False])
            st.rerun()
    
    with col3:
        blue_count = len(st.session_state.grid.get_blue_cells())
        st.metric("Blue Cells", blue_count)
    
    # Create the interactive grid
    st.subheader("Grid")
    
    # Create a DataFrame for display
    grid_data = []
    for y in range(st.session_state.grid.height):
        row = []
        for x in range(st.session_state.grid.width):
            cell = st.session_state.grid.get_cell(x, y)
            row.append("🔵" if cell.is_blue else "⚫")
        grid_data.append(row)
    
    # Display grid with clickable cells
    for y, row in enumerate(grid_data):
        cols = st.columns(len(row))
        for x, cell_symbol in enumerate(row):
            with cols[x]:
                if st.button(cell_symbol, key=f"cell_{x}_{y}", help=f"Cell ({x}, {y})"):
                    st.session_state.grid.toggle_cell(x, y)
                    st.rerun()
    
    # Display grid state as a table
    st.subheader("Grid State")
    df = pd.DataFrame(grid_data)
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()

