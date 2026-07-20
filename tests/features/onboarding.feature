Feature: Onboarding
  As a player, I want to set up my cat before play begins
  so that the game knows its variant and name.

  Background:
    Given the welcome screen is displayed

  @REQ-ONB-001
  Scenario: Only tabby variant is available in Phase 1
    Then the only selectable cat variant is "Tabby"

  @REQ-ONB-002
  Scenario: Start is disabled until a name is entered
    Given the cat variant "Tabby" is selected
    And no name has been entered
    Then the Start button is disabled
    When the player enters the name "Whiskers"
    Then the Start button is enabled

  @REQ-ONB-003
  Scenario: Pressing Start with a variant and name begins the game
    Given the cat variant "Tabby" is selected
    And the cat name "Whiskers" has been entered
    When the player presses Start
    Then the main game screen is displayed
    And the cat's name "Whiskers" is shown on screen
