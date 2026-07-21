Feature: Sleeping
  As a player, I want to put my cat to sleep so that its Energy stat is
  restored over time.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-ANIM-003
  Scenario: Sleep pressed plays falling-asleep animation once
    Given the cat state is "Idle"
    When the player presses the Sleep button
    Then the "falling_asleep" animation plays once

  @REQ-SM-004
  Scenario: Falling Asleep transitions to Sleeping on animation completion
    Given the cat state is "Falling Asleep"
    When the falling-asleep animation completes
    Then the cat state is "Sleeping"

  @REQ-ANIM-004
  Scenario: Sleeping state plays looping sleeping animation
    Given the cat state is "Sleeping"
    Then the "sleeping" animation is playing on loop

  @REQ-ACT-003
  Scenario: Sleep action restores Energy over time
    Given the Energy stat is 3
    And the cat state is "Sleeping"
    When 20 minutes pass
    Then the Energy stat is greater than 3

  @REQ-SM-005
  Scenario: Sleeping transitions to Waking Up when Energy restored
    Given the Energy stat is 9
    And the cat state is "Sleeping"
    When the Energy stat reaches 10
    Then the cat state is "Waking Up"

  @REQ-ANIM-005 @REQ-SM-006
  Scenario: Energy restored plays waking-up animation once, then stretches
    Given the cat state is "Waking Up"
    When the waking-up animation completes
    Then the "waking_up" animation has played once
    And the cat state is "Stretching"

  @REQ-ANIM-012 @REQ-SM-008
  Scenario: Stretch animation plays once, then returns to idle
    Given the cat state is "Stretching"
    When the stretch animation completes
    Then the "stretch" animation has played once
    And the cat state is "Idle"

  @REQ-STAT-008 @REQ-ANIM-009
  Scenario: Energy below 3 triggers sleepy idle animation
    Given the Energy stat is 2
    And the cat state is "Idle"
    Then the "sleepy_idle" animation is playing

  @REQ-AUD-004
  Scenario: No sound effects play during sleep
    Given the cat state is "Sleeping"
    Then no sound effects play
