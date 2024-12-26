import pytest

from fsm_tools.lightweight import ExtFSM
from fsm_tools.exception import ReadError

turnstile = ExtFSM('locked')


def test_fsm_init_success():
    assert isinstance(turnstile.transitions, dict)
    assert turnstile.initial == 'locked'
    assert turnstile.current == turnstile.initial
    assert turnstile.previous is None

def test_fsm_init_dict_failure():
    with pytest.raises(KeyError):
        value = turnstile.transitions['coin']


turnstile.add_transition('locked', 'unlocked', 'coin')
turnstile.add_transition('unlocked', 'locked', 'push')
turnstile.add_transition('locked', 'locked', 'push')
turnstile.add_transition('unlocked', 'unlocked', 'coin')


def test_turnstile_dict_success():
    assert isinstance(turnstile.transitions, dict)
    assert isinstance(turnstile.transitions['locked'], dict)
    assert isinstance(turnstile.transitions['unlocked'], dict)
    assert turnstile.transitions['locked']['coin'] == turnstile.transitions['unlocked']['coin']
    assert turnstile.transitions['unlocked']['push'] == "locked"
    assert turnstile.transitions['locked']['push'] == "locked"


def test_turnstile_dict_failure():
    with pytest.raises(KeyError):
        value = turnstile.transitions['locked']['unlocked']


def test_turnstile_initial_success():
    assert turnstile.initial == "locked"


def test_turnstile_current_success():
    assert turnstile.current == "locked"

def test_turnstile_previous_success():
    assert turnstile.previous is None

def test_turnstile_transitions_coin_success():
    turnstile.trigger('coin')
    assert turnstile.current == "unlocked"

def test_turnstile_transitions_verify_coin_success():
    assert turnstile.initial == "locked"
    assert turnstile.previous == "locked"

def test_turnstile_transitions_plus_coin_success():
    turnstile.trigger('coin')
    assert turnstile.current == "unlocked"
    assert turnstile.previous == "unlocked"
    assert turnstile.initial == "locked"

def test_turnstile_reset_success():
    turnstile.reset()
    assert turnstile.initial == "locked"
    assert turnstile.current == "locked"
    assert turnstile.previous is None

@pytest.mark.parametrize("event, exp_state, exp_previous", [
    ("coin", "unlocked", "locked"),
    ("coin", "unlocked", "unlocked"),
    ("push", "locked", "unlocked"),
    ("coin", "unlocked", "locked"),
    ("coin", "unlocked", "unlocked"),
    ("push", "locked", "unlocked"),
    ("push", "locked", "locked"),
    ("coin", "unlocked", "locked"),
    ("push", "locked", "unlocked"),
    ("coin", "unlocked", "locked"),
    ("coin", "unlocked", "unlocked"),
    ("coin", "unlocked", "unlocked"),
    ("coin", "unlocked", "unlocked"),
    ("coin", "unlocked", "unlocked"),
    ("push", "locked", "unlocked"),
    ("push", "locked", "locked"),
])
def test_turnstile_cycle(event, exp_state, exp_previous):
    turnstile.trigger(event)
    assert turnstile.current == exp_state
    assert turnstile.previous == exp_previous

def test_turnstile_trigger_error():
    previous = turnstile.get_previous()
    with pytest.raises(ReadError):
        turnstile.trigger('pull')
    assert turnstile.previous == previous