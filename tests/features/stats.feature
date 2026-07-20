Feature: Cat Stats
  As a player, I want the cat's Tummy, Happy, and Energy stats to behave
  predictably so that I know when my cat needs attention.

  Background:
    Given a new game has started with the cat named "Whiskers"

  @REQ-STAT-001
  Scenario: All stats start at 10
    Then the Tummy stat is 10
    And the Happy stat is 10
    And the Energy stat is 10

  @REQ-STAT-002
  Scenario: Tummy depletes over time while idle
    Given the Tummy stat is 10
    And the cat state is "Idle"
    When 30 minutes pass
    Then the Tummy stat is less than 10

  @REQ-STAT-003
  Scenario: Happy depletes slower than Tummy while idle
    Given the Tummy stat is 10
    And the Happy stat is 10
    And the cat state is "Idle"
    When 30 minutes pass
    Then the Tummy stat has decreased more than the Happy stat

  @REQ-STAT-005
  Scenario Outline: Stat bar colour matches stat value
    Given the Tummy stat is <value>
    Then the Tummy stat bar is coloured "<colour>"

    Examples:
      | value | colour |
      | 10    | green  |
      | 7     | green  |
      | 6     | yellow |
      | 4     | yellow |
      | 3     | red    |
      | 1     | red    |
