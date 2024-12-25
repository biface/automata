import pytest

from fsm_tools.django import ContextFSM

turnstile = ContextFSM('locked')


def test_fsm_init_success():
    assert isinstance(turnstile.transitions, dict)
    assert turnstile.initial == 'locked'
    assert turnstile.current == turnstile.initial
    assert turnstile.previous is None

def test_fsm_django_context_success():
    assert isinstance(turnstile.as_dict(), dict)
    assert turnstile.as_dict()['current'] == 'locked'


def test_fsm_init_dict_failure():
    with pytest.raises(KeyError):
        value = turnstile.transitions['coin']

def test_fsm_django_context_dict_failure():
    with pytest.raises(KeyError):
        value = turnstile.as_dict()['transition']

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

def test_turnstile_dict_django_context_success():
    assert isinstance(turnstile.as_dict()['transitions'], dict)
    assert isinstance(turnstile.as_dict()['transitions']['locked'], dict)
    assert isinstance(turnstile.as_dict()['transitions']['unlocked'], dict)
    assert turnstile.as_dict()['transitions']['locked']['coin'] == turnstile.as_dict()['transitions']['unlocked']['coin']
    assert turnstile.as_dict()['transitions']['unlocked']['push'] == "locked"
    assert turnstile.as_dict()['transitions']['locked']['push'] == "locked"

def test_turnstile_dict_failure():
    with pytest.raises(KeyError):
        value = turnstile.transitions['locked']['unlocked']

def test_turnstile_dict_django_context_failure():
    with pytest.raises(KeyError):
        value = turnstile.as_dict()['transition']['locked']['unlocked']

def test_turnstile_initial_success():
    assert turnstile.initial == "locked"


def test_turnstile_current_success():
    assert turnstile.current == "locked"

def test_turnstile_current_django_context_success():
    assert turnstile.as_dict()['current'] == 'locked'

def test_turnstile_previous_success():
    assert turnstile.previous is None

def test_turnstile_previous_django_context_success():
    assert turnstile.as_dict()['previous'] is None

def test_turnstile_transitions_coin_success():
    turnstile.trigger('coin')
    assert turnstile.current == "unlocked"

def test_turnstile_transitions_coin_django_context_success():
    assert turnstile.as_dict()['current'] == "unlocked"

def test_turnstile_transitions_verify_coin_success():
    assert turnstile.initial == "locked"
    assert turnstile.previous == "locked"

def test_turnstile_transitions_verify_coin_django_context_success():
    assert turnstile.as_dict()['previous'] == "locked"

def test_turnstile_transitions_plus_coin_success():
    turnstile.trigger('coin')
    assert turnstile.current == "unlocked"
    assert turnstile.previous == "unlocked"
    assert turnstile.initial == "locked"

def test_turnstile_transitions_plus_coin_django_context_success():
    assert turnstile.as_dict()['current'] == "unlocked"
    assert turnstile.as_dict()['previous'] == "unlocked"

def test_turnstile_reset_success():
    turnstile.reset()
    assert turnstile.initial == "locked"
    assert turnstile.current == "locked"
    assert turnstile.previous is None

def test_turnstile_reset_django_context_success():
    assert turnstile.as_dict()['current'] == 'locked'
    assert turnstile.as_dict()['previous'] is None

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
    assert turnstile.as_dict()['current'] == exp_state
    assert turnstile.as_dict()['previous'] == exp_previous
