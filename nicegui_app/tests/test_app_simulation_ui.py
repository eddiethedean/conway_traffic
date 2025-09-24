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
    app.grid.cells[2][1].is_blue = True
    app.grid.cells[2][2].is_blue = True
    app.grid.cells[2][3].is_blue = True
    app.simulation_running = True
    # Simulate timer calling run_simulation_step
    steps = 3
    for _ in range(steps):
        app.run_simulation_step()
    # After 3 steps, the blinker should have oscillated
    assert app.grid.cells[2][2].is_blue, "Center cell should remain blue"
    assert app.grid.cells[1][2].is_blue or app.grid.cells[3][2].is_blue, "Blinker should oscillate vertically"


def test_simulation_can_resume_after_stop(app):
    app.simulation_running = True
    app.run_simulation_step()
    app.stop_simulation()
    assert not app.simulation_running
    app.run_simulation_continuous()
    assert app.simulation_running
