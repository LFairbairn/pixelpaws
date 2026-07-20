Feature: Playing
  As a player, I want to play with my cat so that its Happy stat is
  restored, at the cost of some Energy.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-STAT-004
  Scenario: Energy depletes while playing
    Given the Energy stat is 10
    When the player presses the Play button
    Then the Energy stat is less than 10

  @REQ-ACT-002
  Scenario: Play action restores Happy stat and depletes Energy
    Given the Happy stat is 5
    And the Energy stat is 10
    When the player presses the Play button
    Then the Happy stat is greater than 5
    And the Energy stat is less than 10

  @REQ-STAT-007
  Scenario: Happy below 3 triggers sad state
    Given the Happy stat is 2
    Then the Happy stat is critical

  @REQ-ANIM-007
  Scenario: Play action plays playing animation
    Given the Happy stat is 5
    When the player presses the Play button
    Then the "playing" animation plays once

  @REQ-ANIM-008
  Scenario: Happy critical plays sad animation
    Given the Happy stat is 2
    Then the "sad" animation is playing

  @REQ-AUD-002
  Scenario: Play action plays happy sound
    Given the Happy stat is 5
    When the player presses the Play button
    Then the "happy" sound effect plays
