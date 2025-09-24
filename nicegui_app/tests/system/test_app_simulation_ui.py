import pytest
from app import InteractiveGridApp
import time


@pytest.fixture
def app():
    return InteractiveGridApp(width=5, height=5)


def test_run_button_starts_simulation(app):
    # Set up a blinker pattern
    app.grid.cells[2][1].is_blue = True
    app.grid.cells[2][2].is_blue = True
    app.grid.cells[2][3].is_blue = True
    # Simulate clicking the Run button
    app.run_button_clicked = False
    app.simulation_running = False
    app.run_simulation_continuous()
    assert app.simulation_running, "Simulation should be running after clicking Run"


def test_stop_button_stops_simulation(app):
    app.simulation_running = True
    app.stop_simulation()
    assert not app.simulation_running, "Simulation should stop after clicking Stop"


def test_simulation_advances_automatically(app):
    # Set up a blinker pattern (horizontal line of 3 blue cells)
    app.grid.cells[2][1].is_blue = True
    app.grid.cells[2][2].is_blue = True
    app.grid.cells[2][3].is_blue = True
    # Set color_state to 2 (blue) for Conway's rules to apply
    app.grid.cells[2][1].color_state = 2
    app.grid.cells[2][2].color_state = 2
    app.grid.cells[2][3].color_state = 2

    app.simulation_running = True

    # After 1 step: should become vertical (center column)
    app.run_simulation_step()
    assert app.grid.cells[1][2].is_blue, "Top cell should be blue after 1 step"
    assert app.grid.cells[2][2].is_blue, "Center cell should be blue after 1 step"
    assert app.grid.cells[3][2].is_blue, "Bottom cell should be blue after 1 step"
    assert not app.grid.cells[2][1].is_blue, "Left cell should not be blue after 1 step"
    assert not app.grid.cells[2][
        3
    ].is_blue, "Right cell should not be blue after 1 step"

    # After 2 steps: should return to horizontal (blinker oscillates every 2 steps)
    app.run_simulation_step()
    assert app.grid.cells[2][1].is_blue, "Left cell should be blue after 2 steps"
    assert app.grid.cells[2][2].is_blue, "Center cell should be blue after 2 steps"
    assert app.grid.cells[2][3].is_blue, "Right cell should be blue after 2 steps"
    assert not app.grid.cells[1][2].is_blue, "Top cell should not be blue after 2 steps"
    assert not app.grid.cells[3][
        2
    ].is_blue, "Bottom cell should not be blue after 2 steps"


def test_simulation_can_resume_after_stop(app):
    app.simulation_running = True
    app.run_simulation_step()
    app.stop_simulation()
    assert not app.simulation_running
    app.run_simulation_continuous()
    assert app.simulation_running
