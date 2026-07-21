from pytest_bdd import scenario


@scenario("state_machine.feature", "Idle state plays looping idle animation")
def test_idle_state_plays_looping_idle_animation():
    pass


@scenario(
    "state_machine.feature", "Idle transitions to Falling Asleep when Sleep pressed"
)
def test_idle_transitions_to_falling_asleep_when_sleep_pressed():
    pass


@scenario("state_machine.feature", "Idle transitions to Stretching when triggered")
def test_idle_transitions_to_stretching_when_triggered():
    pass
