Feature: State Machine
  As a developer, I want the cat's state transitions to be well-defined
  so that its behaviour is predictable and testable.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-ANIM-001
  Scenario: Idle state plays looping idle animation
    Given the cat state is "Idle"
    Then the "idle" animation is playing on loop

  @REQ-SM-001
  Scenario: Idle transitions to Meowing when Tummy critical
    Given the cat state is "Idle"
    When the Tummy stat drops to 2
    Then the cat state is "Meowing"

  @REQ-SM-002
  Scenario: Idle transitions to Falling Asleep when Sleep pressed
    Given the cat state is "Idle"
    When the player presses the Sleep button
    Then the cat state is "Falling Asleep"
