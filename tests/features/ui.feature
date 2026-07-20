Feature: UI Layout
  As a young player, I want the screen to clearly show my cat, its name,
  its stats, and the action buttons so the game is easy to use.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-UI-001
  Scenario: Cat name is shown at the top of the screen
    Then the cat's name "Whiskers" is displayed at the top of the screen

  @REQ-UI-002
  Scenario: Cat sprite is shown centred on screen
    Then the cat sprite is displayed in the centre of the screen

  @REQ-UI-003
  Scenario: Stat bars are shown at the bottom of the screen
    Then the Tummy, Happy, and Energy stat bars are displayed at the bottom of the screen

  @REQ-ACT-004
  Scenario: Action buttons are visible on every screen
    Then the Feed, Play, and Sleep buttons are displayed
    And each button is large and labelled with its name and emoji
