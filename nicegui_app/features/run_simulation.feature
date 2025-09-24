Feature: Run Conway's Game of Life simulation

  Scenario: User runs the simulation on a grid
    Given the grid is initialized with width 5 and height 5
    And the user toggles cell (1, 2) to blue
    And the user toggles cell (2, 2) to blue
    And the user toggles cell (3, 2) to blue
    When the user clicks the Run button
    Then cell (2, 1) should be blue
    And cell (2, 2) should be blue
    And cell (2, 3) should be blue
    And all other cells should be black
