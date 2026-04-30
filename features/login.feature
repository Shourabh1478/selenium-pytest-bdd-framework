Feature: Advanced Selenium Concepts

  Scenario: Verify sorting dropdown functionality
    Given the user is logged into SauceDemo
    When the user sorts products by "Name (Z to A)"
    Then the first product should be "Test.allTheThings() T-Shirt (Red)"

  Scenario: Verify Twitter link opens in a new window
    Given the user is logged into SauceDemo
    When the user clicks on the Twitter icon
    Then a new window should open with Twitter