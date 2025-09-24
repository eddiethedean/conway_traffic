Feature: Interactive Grid App Features

  Scenario: Cell color cycling (black -> orange -> blue -> black)
    Given the app is running
    When I click a black cell
    Then the cell should turn orange
    When I click the same cell again
    Then the cell should turn blue
    When I click the same cell again
    Then the cell should turn black

  Scenario: Clear all cells
    Given the app is running
    And I set some cells to orange and blue
    When I click the "Clear All" button
    Then all cells should be black

  Scenario: Save and load grid with blue and orange cells
    Given the app is running
    And I set some cells to orange and blue
    When I click the "Save Grid" button
    And I click the "Clear All" button
    And I click the "Load Grid" button
    Then the previously set orange and blue cells should be restored

  Scenario: Simulation only updates blue cells
    Given the app is running
    And I set some cells to orange and some to blue in a pattern
    When I click the "Run" button
    Then only the blue cells should change according to the rules
    And the orange cells should remain orange

  Scenario: Grid appears on page load
    Given the app is running
    Then the grid should be visible immediately

  Scenario: Resize grid
    Given the app is running
    When I enter new width and height and click "Resize Grid"
    Then the grid should update to the new size

  Scenario: Blue/orange cell count updates
    Given the app is running
    And I set some cells to orange and blue
    Then the orange cell count label should update accordingly
