from pytest_bdd import given, parsers, then, when

from src.cat import Cat
from src.cat_state import CatState


def _state_from_name(name: str) -> CatState:
    return CatState[name.upper().replace(" ", "_")]


@given(
    parsers.parse('a new game has started with the cat named "{name}"'),
    target_fixture="cat",
)
def new_game(name):
    return Cat(name=name)


@given(parsers.parse('the cat state is "{state_name}"'))
def given_cat_state(cat, state_name):
    cat.set_state(_state_from_name(state_name))


@given(parsers.parse("the Energy stat is {value:d}"))
def given_energy(cat, value):
    cat.energy.value = value


@when("the player presses the Sleep button")
def press_sleep(cat):
    cat.press_sleep()


@when("the falling-asleep animation completes")
@when("the waking-up animation completes")
@when("the stretch animation completes")
def animation_completes(cat):
    cat.on_animation_complete()


@when("a stretch is triggered")
def stretch_triggered(cat):
    cat.trigger_stretch()


@when(parsers.parse("{minutes:d} minutes pass"))
def minutes_pass(cat, minutes):
    cat.tick(minutes * 60)


@when(parsers.parse("the Energy stat reaches {value:d}"))
def energy_reaches(cat, value):
    cat.restore_energy(value - cat.energy.value)


@then(parsers.parse('the "{animation_name}" animation plays once'))
def animation_plays_once(cat, animation_name):
    assert cat.current_animation.name == animation_name
    assert cat.current_animation.loop is False


@then(parsers.parse('the "{animation_name}" animation is playing on loop'))
def animation_playing_on_loop(cat, animation_name):
    assert cat.current_animation.name == animation_name
    assert cat.current_animation.loop is True


@then(parsers.parse('the "{animation_name}" animation has played once'))
def animation_has_played_once(cat, animation_name):
    assert cat.last_completed_animation is not None
    assert cat.last_completed_animation.name == animation_name
    assert cat.last_completed_animation.loop is False


@then(parsers.parse('the cat state is "{state_name}"'))
def then_cat_state(cat, state_name):
    assert cat.state == _state_from_name(state_name)


@then(parsers.parse("the Energy stat is greater than {value:d}"))
def energy_greater_than(cat, value):
    assert cat.energy.value > value


@then("no sound effects play")
def no_sound_effects(cat):
    assert cat.sounds_played == []
