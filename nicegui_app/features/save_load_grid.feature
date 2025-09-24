Feature: Save and load grid

  Scenario: User saves a grid and loads it back
    Given the grid is initialized with width 5 and height 5
    When the user toggles cell (2, 2) to blue
    And the user saves the grid
    And the user clears all cells
    And the user loads the grid
    Then cell (2, 2) should be blue
    And all other cells should be black
