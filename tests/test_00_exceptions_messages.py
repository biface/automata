"""
Tests for the message system (utils/json.py) and exception hierarchy (exception.py).

Language: en-US (fixed — i18n-tools integration deferred, see DD-006 / issue #8).
Replaces: test_00_errors_locales.py (locale-dependent tests skipped in v0.0.3).
Related issues: #22, #8.
"""

import pytest

from fsm_tools.utils.json import (
    localized_messages,
    load_message,
    seek_message,
    format_message,
    get_message,
    generate_message,
)
from fsm_tools.exception import (
    AutomatonException,
    AutomatonError,
    AutomatonGroup,
    ReadError,
    AddError,
    RemoveError,
    ModifyError,
    ValidationError,
    SearchError,
    RemoveComponentError,
)
from fsm_tools.constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clear_message_cache():
    """Reset the module-level message cache before each test for isolation."""
    localized_messages.clear()
    yield
    localized_messages.clear()


# ---------------------------------------------------------------------------
# load_message
# ---------------------------------------------------------------------------

class TestLoadMessage:

    def test_loads_automata_domain(self):
        load_message("automata")
        assert "automata" in localized_messages
        assert "en-US" in localized_messages["automata"]

    def test_loads_errors_domain(self):
        load_message("errors")
        assert "errors" in localized_messages
        assert "en-US" in localized_messages["errors"]

    def test_reload_refreshes_cache(self):
        load_message("automata")
        first = id(localized_messages["automata"])
        load_message("automata")
        # dict is replaced — id changes
        assert id(localized_messages["automata"]) != first

    def test_unknown_domain_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError,
                           match="The JSON file for domain 'unknown' was not found."):
            load_message("unknown")


# ---------------------------------------------------------------------------
# seek_message
# ---------------------------------------------------------------------------

class TestSeekMessage:

    @pytest.mark.parametrize("msg_id, domain, expected", [
        ("4101", "automata", "Read the symbols of the alphabet of a finite automaton."),
        ("4605", "automata", "Validate a finite automaton."),
        ("1101", "automata", "Read the symbols of the alphabet of a Turing machine."),
        ("1203", "automata", "Remove a transition from a Turing machine."),
        ("3519", "automata", "Attempted to remove a symbol from an empty stack."),
        ("2605", "automata", "Validate a context-sensitive automaton."),
        ("4101", "errors",   "Unable to read symbols as the alphabet is empty."),
        ("3519", "errors",   "Error: attempt to pop a symbol from an empty stack."),
        ("1506", "errors",   "An infinite loop was detected during execution."),
    ])
    def test_seek_known_message(self, msg_id, domain, expected):
        result = seek_message(msg_id, domain)
        assert result == expected

    def test_lang_parameter_is_ignored(self):
        """lang is a no-op — result must be identical regardless of value."""
        result_default = seek_message("4101", "automata")
        result_with_lang = seek_message("4101", "automata", lang="fr-FR")
        assert result_default == result_with_lang

    def test_unknown_msg_id_raises_key_error(self):
        with pytest.raises(KeyError,
                           match="The message with ID '9999' was not found for language 'en-US'."):
            seek_message("9999", "automata")

    def test_unknown_domain_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError,
                           match="The JSON file for domain 'nope' was not found."):
            seek_message("4101", "nope")

    def test_lazy_load_on_first_call(self):
        assert "automata" not in localized_messages
        seek_message("4101", "automata")
        assert "automata" in localized_messages

    def test_cached_domain_not_reloaded(self):
        seek_message("4101", "automata")
        first_id = id(localized_messages["automata"])
        seek_message("4102", "automata")
        assert id(localized_messages["automata"]) == first_id


# ---------------------------------------------------------------------------
# format_message
# ---------------------------------------------------------------------------

class TestFormatMessage:

    @pytest.mark.parametrize("template, kwargs, expected", [
        ("No placeholders.", {}, "No placeholders."),
        ("Symbol '{symbol}' is invalid.", {"symbol": "X"}, "Symbol 'X' is invalid."),
        ("Rule '{lhs}' -> '{rhs}' is malformed.", {"lhs": "A", "rhs": "b"},
         "Rule 'A' -> 'b' is malformed."),
        ("Reason: {reason}.", {"reason": "empty alphabet"}, "Reason: empty alphabet."),
    ])
    def test_format_known_templates(self, template, kwargs, expected):
        assert format_message(template, **kwargs) == expected

    def test_missing_parameter_raises_value_error(self):
        with pytest.raises(ValueError,
                           match="The parameter 'symbol' is missing for formatting the message."):
            format_message("Symbol '{symbol}' is invalid.")

    def test_extra_parameters_are_ignored(self):
        result = format_message("Hello {name}.", name="World", extra="ignored")
        assert result == "Hello World."


# ---------------------------------------------------------------------------
# get_message
# ---------------------------------------------------------------------------

class TestGetMessage:

    @pytest.mark.parametrize("msg_id, domain, kwargs, expected", [
        ("4101", "automata", {},
         "Read the symbols of the alphabet of a finite automaton."),
        ("4102", "errors", {"symbol": "X"},
         "The symbol 'X' cannot be added as it already exists in the alphabet of the finite automaton."),
        ("1605", "errors", {"reason": "empty tape"},
         "The Turing machine is invalid: empty tape."),
        ("3519", "errors", {},
         "Error: attempt to pop a symbol from an empty stack."),
        ("4203", "errors", {"transition": "q0->q1"},
         "Unable to remove the transition 'q0->q1' as it does not exist in the finite automaton."),
    ])
    def test_get_known_message(self, msg_id, domain, kwargs, expected):
        assert get_message(msg_id, domain, **kwargs) == expected

    def test_lang_parameter_is_ignored(self):
        r1 = get_message("4101", "automata")
        r2 = get_message("4101", "automata", lang="de-DE")
        assert r1 == r2

    def test_unknown_msg_id_raises_key_error(self):
        with pytest.raises(KeyError):
            get_message("0000", "automata")

    def test_missing_format_parameter_raises_value_error(self):
        with pytest.raises(ValueError,
                           match="The parameter 'symbol' is missing for formatting the message."):
            get_message("4102", "errors")  # requires {symbol}


# ---------------------------------------------------------------------------
# generate_message
# ---------------------------------------------------------------------------

class TestGenerateMessage:

    @pytest.mark.parametrize("grammar, component, action, domain, kwargs, expected", [
        ("Regular", "alphabet", "read", "automata", {},
         "Read the symbols of the alphabet of a finite automaton."),
        ("Regular", "alphabet", "add", "automata", {},
         "Add a symbol to the alphabet of a finite automaton."),
        ("Recursively Enumerable", "alphabet", "read", "automata", {},
         "Read the symbols of the alphabet of a Turing machine."),
        ("Context-Free", "stack", "withdraw", "automata", {},
         "Attempted to remove a symbol from an empty stack."),
        ("Context-Sensitive", "validation", "validate", "automata", {},
         "Validate a context-sensitive automaton."),
        ("Regular", "alphabet", "add", "errors", {"symbol": "Z"},
         "The symbol 'Z' cannot be added as it already exists in the alphabet of the finite automaton."),
        ("Recursively Enumerable", "validation", "validate", "errors", {"reason": "loop"},
         "The Turing machine is invalid: loop."),
    ])
    def test_generate_known_message(self, grammar, component, action, domain, kwargs, expected):
        result = generate_message(grammar, component, action, domain, **kwargs)
        assert result == expected

    def test_lang_parameter_is_ignored(self):
        r1 = generate_message("Regular", "alphabet", "read", "automata")
        r2 = generate_message("Regular", "alphabet", "read", "automata", lang="fr-FR")
        assert r1 == r2

    def test_invalid_component_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown component name"):
            generate_message("Regular", "rules", "read", "automata")

    def test_invalid_grammar_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown grammar name"):
            generate_message("Unknown", "alphabet", "read", "automata")

    def test_unknown_domain_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError,
                           match="The JSON file for domain 'bogus' was not found."):
            generate_message("Regular", "alphabet", "read", "bogus")

    def test_missing_format_parameter_raises_value_error(self):
        # errors/Regular/alphabet/add requires {symbol}
        with pytest.raises(ValueError,
                           match="The parameter 'symbol' is missing for formatting the message."):
            generate_message("Regular", "alphabet", "add", "errors")


# ---------------------------------------------------------------------------
# AutomatonException — base class
# ---------------------------------------------------------------------------

class TestAutomatonException:

    def test_valid_construction(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        assert exc.grammar == "Regular"
        assert exc.component == "alphabet"
        assert exc.action == "read"
        assert exc.message is not None
        assert isinstance(exc.message, str)

    def test_error_code_computation(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        expected = (
            1000 * CHOMSKY_GRAMMARS["Regular"]
            + 100 * COMPONENTS["alphabet"]
            + ACTIONS["read"]
        )
        assert exc.value == expected

    @pytest.mark.parametrize("grammar, component, action", [
        ("Regular", "alphabet", "read"),
        ("Context-Free", "stack", "withdraw"),
        ("Context-Sensitive", "validation", "validate"),
        ("Recursively Enumerable", "alphabet", "read"),
    ])
    def test_all_chomsky_levels(self, grammar, component, action):
        exc = AutomatonException(grammar, component, action)
        assert exc.grammar == grammar

    def test_invalid_grammar_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown grammar hierarchy name."):
            AutomatonException("Unknown", "alphabet", "read")

    def test_invalid_component_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown component name."):
            AutomatonException("Regular", "rules", "read")

    def test_invalid_action_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown action name."):
            AutomatonException("Regular", "alphabet", "fly")

    def test_locale_parameter_is_accepted_but_no_op(self):
        exc1 = AutomatonException("Regular", "alphabet", "read")
        exc2 = AutomatonException("Regular", "alphabet", "read", locale="fr-FR")
        assert exc1.message == exc2.message

    def test_str_returns_message(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        assert str(exc) == exc.message

    def test_group_contains_self(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        assert exc in exc.group.exceptions

    def test_set_locale_updates_locale_attribute(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        exc.set_locale("fr-FR")
        assert exc.locale == "fr-FR"

    def test_generate_message_returns_string(self):
        exc = AutomatonException("Regular", "alphabet", "read")
        msg = exc.generate_message(None)
        assert isinstance(msg, str)
        assert len(msg) > 0


# ---------------------------------------------------------------------------
# AutomatonGroup
# ---------------------------------------------------------------------------

class TestAutomatonGroup:

    def test_add_exception(self):
        group = AutomatonGroup()
        exc = ValueError("test")
        group.add_exception(exc)
        assert exc in group.exceptions

    def test_multiple_exceptions(self):
        group = AutomatonGroup()
        for i in range(3):
            group.add_exception(ValueError(str(i)))
        assert len(group.exceptions) == 3


# ---------------------------------------------------------------------------
# Specialised exception classes
# ---------------------------------------------------------------------------

class TestSpecialisedExceptions:

    @pytest.mark.parametrize("cls, component, action", [
        (ReadError,            "alphabet",   "read"),
        (AddError,             "alphabet",   "add"),
        (RemoveError,          "alphabet",   "remove"),
        (ModifyError,          "alphabet",   "modify"),
        (ValidationError,      "validation", "validate"),
        (SearchError,          "validation", "search"),
        (RemoveComponentError, "stack",      "withdraw"),
    ])
    def test_action_attribute(self, cls, component, action):
        grammar = "Context-Free" if cls is RemoveComponentError else "Regular"
        exc = cls(grammar, component)
        assert exc.action == action

    @pytest.mark.parametrize("cls, component", [
        (ReadError,            "alphabet"),
        (AddError,             "alphabet"),
        (RemoveError,          "alphabet"),
        (ModifyError,          "alphabet"),
        (ValidationError,      "validation"),
        (SearchError,          "validation"),
        (RemoveComponentError, "stack"),
    ])
    def test_is_automaton_error(self, cls, component):
        grammar = "Context-Free" if cls is RemoveComponentError else "Regular"
        exc = cls(grammar, component)
        assert isinstance(exc, AutomatonError)
        assert isinstance(exc, AutomatonException)

    @pytest.mark.parametrize("cls, grammar, component", [
        (ReadError,            "Recursively Enumerable", "alphabet"),
        (AddError,             "Context-Free",           "stack"),
        (RemoveError,          "Context-Sensitive",      "states"),
        (ModifyError,          "Regular",                "transitions"),
        (ValidationError,      "Regular",                "validation"),
        (SearchError,          "Context-Free",           "validation"),
        (RemoveComponentError, "Context-Free",           "stack"),
    ])
    def test_grammar_and_component(self, cls, grammar, component):
        exc = cls(grammar, component)
        assert exc.grammar == grammar
        assert exc.component == component

    def test_read_error_with_event(self):
        exc = ReadError("Regular", "alphabet", symbol="X")
        assert isinstance(exc, ReadError)
        assert exc.message is not None

    def test_add_error_with_event(self):
        exc = AddError("Regular", "alphabet", symbol="X")
        assert isinstance(exc, AddError)

    def test_remove_error_with_event(self):
        exc = RemoveError("Regular", "states", symbol="q0")
        assert isinstance(exc, RemoveError)

    def test_validation_error_with_event(self):
        exc = ValidationError("Regular", "validation", reason="empty alphabet")
        assert isinstance(exc, ValidationError)

    def test_locale_no_op_on_specialised(self):
        exc1 = ReadError("Regular", "alphabet")
        exc2 = ReadError("Regular", "alphabet", locale="de-DE")
        assert exc1.message == exc2.message
