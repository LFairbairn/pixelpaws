Feature: Feeding
  As a player, I want to feed my cat so that its Tummy stat is restored
  and it stops meowing.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-STAT-006
  Scenario: Tummy below 3 is critical
    Given the Tummy stat is 2
    Then the Tummy stat is critical

  @REQ-ACT-001
  Scenario: Feed action restores Tummy stat to full
    Given the Tummy stat is 4
    When the player presses the Feed button
    Then the Tummy stat is 10

  @REQ-ANIM-002
  Scenario: Tummy critical plays meow animation
    Given the Tummy stat is 2
    Then the "meow" animation is playing on loop

  @REQ-SM-003
  Scenario: Meowing returns to Idle once Tummy is restored
    Given the Tummy stat is 2
    And the cat state is "Meowing"
    When the player presses the Feed button
    Then the cat state is "Idle"

  @REQ-ANIM-006
  Scenario: Feed action plays eating animation
    Given the Tummy stat is 5
    When the player presses the Feed button
    Then the "eating" animation plays once

  @REQ-AUD-001
  Scenario: Tummy critical plays meow sound
    Given the Tummy stat is 2
    Then the "meow" sound effect plays

  @REQ-AUD-003
  Scenario: Feed action plays eating sound
    Given the Tummy stat is 5
    When the player presses the Feed button
    Then the "eating" sound effect plays
