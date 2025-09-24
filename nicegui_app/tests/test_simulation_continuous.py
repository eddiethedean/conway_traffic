import pytest
import time
from unittest.mock import patch
from grid_persistence import Grid, run_conway_step

class DummyApp:
    def __init__(self, width=5, height=5):
        self.grid = Grid(width, height)
        self.running = False
        self.steps = 0

    def run_simulation_step(self):
        self.grid = run_conway_step(self.grid)
        self.steps += 1

    def start_simulation(self):
        self.running = True

    def stop_simulation(self):
        self.running = False


def test_simulation_runs_continuously(monkeypatch):
    app = DummyApp()
    app.grid.cells[2][1].is_blue = True
    app.grid.cells[2][2].is_blue = True
    app.grid.cells[2][3].is_blue = True

    # Simulate timer calling run_simulation_step every 0.1s
    app.start_simulation()
    for _ in range(5):
        if app.running:
            app.run_simulation_step()
    assert app.steps == 5


def test_simulation_stops_when_user_clicks_stop():
    app = DummyApp()
    app.start_simulation()
    for i in range(3):
        if app.running:
            app.run_simulation_step()
        if i == 1:
            app.stop_simulation()
    assert app.steps == 2
    assert not app.running


def test_simulation_can_resume():
    app = DummyApp()
    app.start_simulation()
    app.run_simulation_step()
    app.stop_simulation()
    app.start_simulation()
    app.run_simulation_step()
    assert app.steps == 2
    assert app.running
