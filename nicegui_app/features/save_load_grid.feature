Feature: Save and Load Grid

  Scenario: Save and load grid with blue and orange cells
    Given the app is running
    And I set some cells to orange and blue
    When I click the "Save Pattern" button
    And I click the "Clear All" button
    And I click the "Load Pattern" button
    Then the previously set orange and blue cells should be restored
