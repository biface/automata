import pytest
from fsm_tools.exception import (
    AutomatonException,
    ReadError,
    AddError,
    RemoveError,
    ModifyError,
    ValidationError,
    SearchError,
)
from fsm_tools.constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS

# Test fixture to provide valid and invalid input
@pytest.fixture
def valid_inputs():
    return {
        "grammar": "Regular",
        "component": "alphabet",
        "action": "read",
        "locale": "en-US",
    }

@pytest.fixture
def invalid_inputs():
    return {
        "grammar": "Unknown",
        "component": "invalid_component",
        "action": "nonexistent_action",
        "locale": "en-US",
    }

# Test: AutomatonException initialization
def test_automaton_exception_initialization(valid_inputs):
    exc = AutomatonException(
        grammar=valid_inputs["grammar"],
        component=valid_inputs["component"],
        action=valid_inputs["action"],
        locale=valid_inputs["locale"]
    )
    assert exc.message is not None
    assert exc.grammar == valid_inputs["grammar"]
    assert exc.component == valid_inputs["component"]
    assert exc.action == valid_inputs["action"]

# Test: AutomatonException with invalid inputs
@pytest.mark.parametrize("grammar, component, action", [
    ("Unknown", "alphabet", "read"),
    ("Regular", "unknown_component", "add"),
    ("Regular", "alphabet", "unknown_action"),
])
def test_automaton_exception_invalid_inputs(grammar, component, action):
    with pytest.raises(ValueError):
        AutomatonException(grammar=grammar, component=component, action=action)

# Test: Specialized Exceptions
@pytest.mark.parametrize("exception_cls, action", [
    (ReadError, "read"),
    (AddError, "add"),
    (RemoveError, "remove"),
    (ModifyError, "modify"),
])
def test_specialized_exceptions(exception_cls, action, valid_inputs):
    exc = exception_cls(
        grammar_level=valid_inputs["grammar"],
        component=valid_inputs["component"],
        locale=valid_inputs["locale"]
    )
    assert exc.message is not None
    assert exc.action == action

# Test : Specific actions

@pytest.mark.parametrize("exception_cls, grammar, component, action", [
    (ValidationError, "Regular", "validation", "validate"),
    (SearchError, "Context-Free", "validation", "search"),
])
def test_specialized_exceptions(exception_cls, grammar, component, action):
    exc = exception_cls(
        grammar_level=grammar,
        component=component,
        locale="en-US"
    )
    assert exc.message is not None
    assert exc.action == action

# Test: Locale updates
def test_exception_locale_update(valid_inputs):
    exc = AutomatonException(
        grammar=valid_inputs["grammar"],
        component=valid_inputs["component"],
        action=valid_inputs["action"],
        locale=valid_inputs["locale"]
    )
    new_locale = "fr-FR"
    exc.set_locale(new_locale)
    assert exc.locale == new_locale
    assert exc.message == exc.generate_message(new_locale)

# Test: Error code calculation
def test_error_code_calculation(valid_inputs):
    exc = AutomatonException(
        grammar=valid_inputs["grammar"],
        component=valid_inputs["component"],
        action=valid_inputs["action"],
        locale=valid_inputs["locale"]
    )
    expected_code = 1000 * CHOMSKY_GRAMMARS[valid_inputs["grammar"]] + \
                    100 * COMPONENTS[valid_inputs["component"]] + \
                    ACTIONS[valid_inputs["action"]]
    assert exc.value == expected_code