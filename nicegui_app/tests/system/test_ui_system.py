"""System tests for UI components and user interactions."""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from app import InteractiveGridApp


class TestUIInitialization:
    """Test UI component initialization and setup."""
    
    def test_app_ui_components_initialized(self):
        """Test that all UI components are properly initialized."""
        app = InteractiveGridApp(width=5, height=5)
        
        # UI components should be None before create_ui is called
        assert app.width_input is None
        assert app.height_input is None
        assert app.traffic_count_label is None
        assert app.grid_container is None
        assert app.run_button is None
    
    @patch('app.ui')
    def test_create_ui_sets_up_all_components(self, mock_ui):
        """Test that create_ui properly sets up all UI components."""
        app = InteractiveGridApp(width=5, height=5)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify UI components are created
        assert app.width_input is not None
        assert app.height_input is not None
        assert app.traffic_count_label is not None
        assert app.grid_container is not None
        assert app.run_button is not None
        
        # Verify UI methods were called
        mock_ui.page_title.assert_called_once_with("Conway Traffic Simulation")
        mock_ui.html.assert_called()
        mock_ui.number.assert_called()
        mock_ui.button.assert_called()
        mock_ui.label.assert_called()
    
    @patch('app.ui')
    def test_page_title_and_header_content(self, mock_ui):
        """Test that page title and header content are set correctly."""
        app = InteractiveGridApp()
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify page title
        mock_ui.page_title.assert_called_once_with("Conway Traffic Simulation")
        
        # Verify header content
        html_calls = [call[0][0] for call in mock_ui.html.call_args_list]
        assert any("🚗 Conway Traffic Simulation" in call for call in html_calls)
        assert any("Click cells to cycle" in call for call in html_calls)


class TestUIButtonInteractions:
    """Test button click interactions and their effects."""
    
    @patch('app.ui')
    def test_resize_button_click(self, mock_ui):
        """Test resize button functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_width_input = Mock()
        mock_width_input.value = 5
        mock_height_input = Mock()
        mock_height_input.value = 4
        app.width_input = mock_width_input
        app.height_input = mock_height_input
        
        # Mock other UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Test resize
        app.resize_grid()
        
        # Verify grid was resized
        assert app.grid.width == 5
        assert app.grid.height == 4
        assert app.width == 5
        assert app.height == 4
    
    @patch('app.ui')
    def test_clear_all_button_click(self, mock_ui):
        """Test clear all button functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set some cells to non-black state
        app.grid.cycle_cell_color(1, 1)
        app.grid.cycle_cell_color(2, 2)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify cells are not black initially
        assert not app.grid.get_cell(1, 1).is_black()
        assert not app.grid.get_cell(2, 2).is_black()
        
        # Test clear all
        app.clear_all()
        
        # Verify all cells are now black
        for row in app.grid.cells:
            for cell in row:
                assert cell.is_black()
    
    @patch('app.ui')
    @patch('app.ui.notify')
    def test_save_button_click(self, mock_notify, mock_ui):
        """Test save button functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set up some cell states
        app.grid.cycle_cell_color(1, 1)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Test save
        app.save_grid()
        
        # Verify notification was shown
        mock_notify.assert_called_once()
        assert "saved" in mock_notify.call_args[0][0].lower()
    
    @patch('app.ui')
    @patch('app.ui.notify')
    def test_load_button_click_success(self, mock_notify, mock_ui):
        """Test load button functionality when file exists."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_width_input = Mock()
        mock_height_input = Mock()
        app.width_input = mock_width_input
        app.height_input = mock_height_input
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Create a test file
        app.grid.cycle_cell_color(1, 1)
        app.save_grid()
        
        # Clear the grid
        app.clear_all()
        assert app.grid.get_cell(1, 1).is_black()
        
        # Test load
        app.load_grid()
        
        # Verify notification was shown
        mock_notify.assert_called_once()
        assert "loaded" in mock_notify.call_args[0][0].lower()
        
        # Verify input values were updated
        mock_width_input.value = app.width
        mock_height_input.value = app.height


class TestGridUIInteraction:
    """Test grid UI interactions and cell clicking."""
    
    @patch('app.ui')
    def test_cell_click_updates_grid(self, mock_ui):
        """Test that clicking a cell updates the grid state."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify initial state
        cell = app.grid.get_cell(1, 1)
        assert cell.is_black()
        
        # Simulate cell click
        app.on_cell_click(1, 1)
        
        # Verify cell state changed
        cell = app.grid.get_cell(1, 1)
        assert cell.is_orange()
    
    @patch('app.ui')
    def test_cell_click_cycling(self, mock_ui):
        """Test that cell clicking cycles through all states."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        cell = app.grid.get_cell(1, 1)
        
        # First click: black -> orange
        app.on_cell_click(1, 1)
        assert cell.is_orange()
        
        # Second click: orange -> blue
        app.on_cell_click(1, 1)
        assert cell.is_blue_traffic()
        
        # Third click: blue -> black
        app.on_cell_click(1, 1)
        assert cell.is_black()
    
    @patch('app.ui')
    def test_traffic_count_updates_on_cell_click(self, mock_ui):
        """Test that traffic count label updates when cells are clicked."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_traffic_label = Mock()
        app.traffic_count_label = mock_traffic_label
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify initial count
        app.update_traffic_count()
        mock_traffic_label.text = "Active traffic elements: 0"
        
        # Click a cell to make it active
        app.on_cell_click(1, 1)
        
        # Verify count was updated
        mock_traffic_label.text = "Active traffic elements: 1"


class TestSimulationUI:
    """Test simulation UI interactions and controls."""
    
    @patch('app.ui')
    def test_run_button_text_changes(self, mock_ui):
        """Test that run button text changes during simulation."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_run_button = Mock()
        app.run_button = mock_run_button
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Verify initial button text
        assert app.run_button.text == "Start Simulation"
        
        # Start simulation
        app.run_simulation_continuous()
        
        # Verify button text changed
        assert app.run_button.text == "Stop"
        
        # Stop simulation
        app.stop_simulation()
        
        # Verify button text changed back
        assert app.run_button.text == "Run"
    
    @patch('app.ui')
    def test_toggle_simulation_functionality(self, mock_ui):
        """Test the toggle simulation functionality."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_run_button = Mock()
        app.run_button = mock_run_button
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Initially not running
        assert not app.simulation_running
        
        # Toggle to start
        app.toggle_simulation()
        assert app.simulation_running
        
        # Toggle to stop
        app.toggle_simulation()
        assert not app.simulation_running


class TestInputValidation:
    """Test input validation and error handling."""
    
    @patch('app.ui')
    def test_resize_with_invalid_input(self, mock_ui):
        """Test resize with invalid input values."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components with invalid values
        mock_width_input = Mock()
        mock_width_input.value = -5  # Invalid
        mock_height_input = Mock()
        mock_height_input.value = 0  # Invalid
        app.width_input = mock_width_input
        app.height_input = mock_height_input
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Test resize with invalid input
        app.resize_grid()
        
        # Verify grid size didn't change
        assert app.grid.width == 3
        assert app.grid.height == 3
    
    @patch('app.ui')
    def test_resize_with_missing_inputs(self, mock_ui):
        """Test resize when input components are None."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Set inputs to None
        app.width_input = None
        app.height_input = None
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Test resize with missing inputs
        app.resize_grid()
        
        # Verify grid size didn't change (should return early)
        assert app.grid.width == 3
        assert app.grid.height == 3


class TestGridRendering:
    """Test grid rendering and visual updates."""
    
    @patch('app.ui')
    def test_create_grid_clears_container(self, mock_ui):
        """Test that create_grid clears the container before recreating."""
        app = InteractiveGridApp(width=2, height=2)
        
        # Mock UI components
        mock_container = Mock()
        app.grid_container = mock_container
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        mock_ui.html.return_value = Mock()
        
        app.create_ui()
        
        # Call create_grid
        app.create_grid()
        
        # Verify container was cleared
        mock_container.clear.assert_called_once()
    
    @patch('app.ui')
    def test_grid_css_injected(self, mock_ui):
        """Test that grid CSS is injected when creating the grid."""
        app = InteractiveGridApp(width=2, height=2)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        mock_ui.html.return_value = Mock()
        
        app.create_ui()
        
        # Call create_grid
        app.create_grid()
        
        # Verify CSS was added
        mock_ui.add_head_html.assert_called()
    
    @patch('app.ui')
    def test_cell_html_generation(self, mock_ui):
        """Test that cell HTML is generated with correct classes."""
        app = InteractiveGridApp(width=2, height=2)
        
        # Mock UI components
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        mock_cell_div = Mock()
        mock_ui.html.return_value = mock_cell_div
        
        app.create_ui()
        
        # Set up different cell states
        app.grid.get_cell(0, 0).set_color_state(0)  # black
        app.grid.get_cell(1, 0).set_color_state(1)  # orange
        app.grid.get_cell(0, 1).set_color_state(2)  # blue
        
        # Call create_grid
        app.create_grid()
        
        # Verify HTML calls were made for each cell
        assert mock_ui.html.call_count >= 4  # 2x2 grid = 4 cells
        
        # Verify click handlers were attached
        assert mock_cell_div.on.call_count >= 4


class TestUIStateConsistency:
    """Test that UI state remains consistent with application state."""
    
    @patch('app.ui')
    def test_ui_updates_after_grid_operations(self, mock_ui):
        """Test that UI updates after grid operations."""
        app = InteractiveGridApp(width=3, height=3)
        
        # Mock UI components
        mock_traffic_label = Mock()
        app.traffic_count_label = mock_traffic_label
        
        mock_ui.number.return_value = Mock()
        mock_ui.button.return_value = Mock()
        mock_ui.label.return_value = Mock()
        mock_ui.column.return_value = Mock()
        mock_ui.row.return_value.__enter__ = Mock()
        mock_ui.row.return_value.__exit__ = Mock()
        
        app.create_ui()
        
        # Perform various grid operations
        app.grid.cycle_cell_color(1, 1)
        app.grid.cycle_cell_color(2, 2)
        
        # Verify UI is updated
        app.update_traffic_count()
        mock_traffic_label.text = "Active traffic elements: 2"
        
        # Clear all and verify UI updates
        app.clear_all()
        app.update_traffic_count()
        mock_traffic_label.text = "Active traffic elements: 0"
