Feature: Mouse Drag to Change Grid Cell Colors

  As a user of the Conway Traffic Simulation
  I want to be able to click and drag my mouse across multiple cells
  So that I can quickly change multiple cell colors without clicking each one individually

  Background:
    Given the app is running
    And the grid is displayed

  Scenario: Drag to change cells from black to orange
    Given I have a grid with all black cells
    When I click and hold on cell (2, 2)
    And I drag my mouse to cell (4, 4)
    And I release the mouse button
    Then cells (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), and (4, 4) should be orange
    And all other cells should remain black

  Scenario: Drag to change cells from black to orange (first cycle)
    Given I have a grid with all black cells
    When I click and hold on cell (1, 1)
    And I drag my mouse to cell (3, 3)
    And I release the mouse button
    Then cells (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), and (3, 3) should be orange
    And all other cells should remain black

  Scenario: Drag to cycle through color states
    Given I have a grid with all black cells
    When I click and hold on cell (0, 0)
    And I drag my mouse to cell (2, 2)
    And I release the mouse button
    Then cells (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), and (2, 2) should be orange
    When I click and hold on cell (0, 0)
    And I drag my mouse to cell (2, 2)
    And I release the mouse button
    Then cells (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), and (2, 2) should be blue
    When I click and hold on cell (0, 0)
    And I drag my mouse to cell (2, 2)
    And I release the mouse button
    Then cells (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), and (2, 2) should be black

  Scenario: Drag in different directions
    Given I have a grid with all black cells
    When I click and hold on cell (1, 1)
    And I drag my mouse horizontally to cell (3, 1)
    And I release the mouse button
    Then cells (1, 1), (2, 1), and (3, 1) should be orange
    And all other cells should remain black

  Scenario: Drag vertically
    Given I have a grid with all black cells
    When I click and hold on cell (1, 1)
    And I drag my mouse vertically to cell (1, 3)
    And I release the mouse button
    Then cells (1, 1), (1, 2), and (1, 3) should be orange
    And all other cells should remain black

  Scenario: Drag diagonally
    Given I have a grid with all black cells
    When I click and hold on cell (0, 0)
    And I drag my mouse diagonally to cell (2, 2)
    And I release the mouse button
    Then cells (0, 0), (1, 1), and (2, 2) should be orange
    And all other cells should remain black

  Scenario: Drag with existing colored cells
    Given I have a grid with all black cells
    And cell (1, 1) is already orange
    And cell (2, 2) is already blue
    When I click and hold on cell (0, 0)
    And I drag my mouse to cell (2, 2)
    And I release the mouse button
    Then cells (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), and (2, 1) should be orange
    And cell (1, 1) should be blue (cycled from orange)
    And cell (2, 2) should be black (cycled from blue)
    And all other cells should remain black

  Scenario: Drag outside grid boundaries
    Given I have a grid with all black cells
    When I click and hold on cell (0, 0)
    And I drag my mouse to cell (10, 10) which is outside the grid
    And I release the mouse button
    Then only cells within the grid boundaries should be affected
    And the drag should stop at the grid edge

  Scenario: Drag with simulation running
    Given the app is running
    And I have a grid with all black cells
    And the simulation is running
    When I click and hold on cell (1, 1)
    And I drag my mouse to cell (3, 3)
    And I release the mouse button
    Then the dragged cells should be colored orange
    And the simulation should continue running
    And the traffic count should update to reflect the new colored cells
