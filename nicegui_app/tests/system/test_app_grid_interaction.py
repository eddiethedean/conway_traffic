import pytest
from app import InteractiveGridApp


@pytest.fixture
def app():
    return InteractiveGridApp(width=5, height=5)


def test_click_cell_toggles_color(app):
    # Test the three-state color cycling: black -> orange -> blue -> black
    cell = app.grid.get_cell(2, 2)
    assert not cell.is_blue
    assert not hasattr(cell, "color_state") or cell.color_state == 0

    # First click: black -> orange
    app.on_cell_click(2, 2)
    cell = app.grid.get_cell(2, 2)
    assert cell.is_blue  # Orange cells have is_blue=True
    assert cell.color_state == 1

    # Second click: orange -> blue
    app.on_cell_click(2, 2)
    cell = app.grid.get_cell(2, 2)
    assert cell.is_blue  # Blue cells also have is_blue=True
    assert cell.color_state == 2

    # Third click: blue -> black
    app.on_cell_click(2, 2)
    cell = app.grid.get_cell(2, 2)
    assert not cell.is_blue
    assert cell.color_state == 0


def test_clear_all_resets_grid(app):
    app.grid.get_cell(1, 1).is_blue = True
    app.grid.get_cell(2, 2).is_blue = True
    app.clear_all()
    for row in app.grid.cells:
        for cell in row:
            assert not cell.is_blue


def test_save_and_load_grid(app, tmp_path):
    app.grid.get_cell(1, 1).is_blue = True
    app.grid.get_cell(2, 2).is_blue = True
    save_path = tmp_path / "test_grid.json"
    app.save_path = str(save_path)
    app.save_grid()
    app.clear_all()
    app.load_grid()
    assert app.grid.get_cell(1, 1).is_blue
    assert app.grid.get_cell(2, 2).is_blue
    for y, row in enumerate(app.grid.cells):
        for x, cell in enumerate(row):
            if (x, y) not in [(1, 1), (2, 2)]:
                assert not cell.is_blue
