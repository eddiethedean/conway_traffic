"""CSS styles for Conway Traffic simulation UI."""

GRID_CSS = """
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
