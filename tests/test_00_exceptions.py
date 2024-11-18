import pytest

from fsm_tools.exception import StateMachineException, StateMachineTypeError, StateMachineValueError

state_machine_exception = StateMachineException("Exception message", 3450)

def test_state_machine_exception():
    assert state_machine_exception.code == 3450
    assert state_machine_exception.args[0] == "Exception message"

def test_state_machine_type_error_failure():
    with pytest.raises(ValueError):
        StateMachineTypeError("Exception message", 3450)

state_machine_type_error = StateMachineTypeError("Exception message", 450)

def test_state_machine_type_error_success():
    assert state_machine_type_error.code == 1450
    assert state_machine_type_error.args[0] == "Exception message"

def test_state_machine_value_error_failure():
    with pytest.raises(ValueError):
        StateMachineValueError("Exception message", 3450)

state_machine_value_error = StateMachineValueError("Exception message", 450)

def test_state_machine_value_error_success():
    assert state_machine_value_error.code == 2450
    assert state_machine_value_error.args[0] == "Exception message"