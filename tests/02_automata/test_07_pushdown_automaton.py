"""
Tests for PushdownAutomaton (Type 2 — Context-Free).

Classic example: recogniser for the language L = { aⁿbⁿ | n ≥ 1 }.

Grammar:
    - Input alphabet: {a, b}
    - Stack alphabet: {Z, A}  (Z = bottom marker, A = stack symbol for 'a')
    - States: {q0, q1, q2, OK, nOK}
    - Start state: q0
    - Acceptance: by empty stack

Transitions:
    (q0, a, Z, q0, [A, Z])  — read 'a', keep Z, push A on top
    (q0, a, A, q0, [A, A])  — read 'a', keep A, push another A
    (q0, b, A, q1, [])      — read first 'b', pop A (switch to q1)
    (q1, b, A, q1, [])      — read subsequent 'b', pop A
    (q1, b, Z, q2, [])      — pop the bottom marker → empty stack → accept
"""

import pytest

from fsm_tools import PushdownAutomaton
from fsm_tools.exception import (
    AddError,
    ReadError,
    RemoveComponentError,
    ValidationError,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def pda_anbn():
    """
    PDA for L = { aⁿbⁿ | n ≥ 1 }.
    Acceptance by empty stack.
    """
    pda = PushdownAutomaton(
        name="anbn",
        stack_alphabet={"A"},
        bottom_symbol="Z",
        accept="OK",
        reject="nOK",
    )
    pda.add_terminals("a", "b")
    pda.set_register("q0")
    pda.add_non_terminals("q1", "q2")

    pda.add_transition("q0", "a", "Z", "q0", ["A", "Z"])
    pda.add_transition("q0", "a", "A", "q0", ["A", "A"])
    pda.add_transition("q0", "b", "A", "q1", [])
    pda.add_transition("q1", "b", "A", "q1", [])
    pda.add_transition("q1", "b", "Z", "q2", [])

    return pda


@pytest.fixture
def empty_pda():
    """Minimal unconfigured PDA."""
    return PushdownAutomaton(name="empty")


# ---------------------------------------------------------------------------
# Initialisation tests
# ---------------------------------------------------------------------------


class TestPushdownAutomatonInit:
    def test_init_default(self, empty_pda):
        """Default init sets GRAMMAR, TYPE, stack, and bottom marker."""
        assert empty_pda.GRAMMAR == "Context-Free"
        assert empty_pda.TYPE == 2
        assert empty_pda.stack == ["Z"]
        assert empty_pda.bottom_symbol == "Z"
        assert empty_pda.register == ""
        assert empty_pda.input_word == []
        assert empty_pda.input_pos == 0

    def test_init_custom_bottom(self):
        pda = PushdownAutomaton(name="custom", bottom_symbol="$")
        assert pda.bottom_symbol == "$"
        assert pda.stack == ["$"]
        assert "$" in pda.stack_alphabet

    def test_init_stack_alphabet(self):
        pda = PushdownAutomaton(name="p", stack_alphabet={"A", "B"})
        assert "A" in pda.stack_alphabet
        assert "B" in pda.stack_alphabet
        assert "Z" in pda.stack_alphabet  # bottom marker always present

    def test_accept_reject_states_in_grammar(self, empty_pda):
        assert "OK" in empty_pda.grammar.states
        assert "nOK" in empty_pda.grammar.states

    def test_custom_accept_reject(self):
        pda = PushdownAutomaton(name="p", accept="ACCEPT", reject="REJECT")
        assert pda.validation == {"accept": "ACCEPT", "reject": "REJECT"}
        assert "ACCEPT" in pda.grammar.states
        assert "REJECT" in pda.grammar.states

    def test_isinstance_hierarchy(self, empty_pda):
        """PDA must satisfy the formal Chomsky hierarchy membership."""
        from fsm_tools import Automaton, LinearBoundedAutomaton, TuringMachine

        assert isinstance(empty_pda, LinearBoundedAutomaton)
        assert isinstance(empty_pda, TuringMachine)
        assert isinstance(empty_pda, Automaton)


# ---------------------------------------------------------------------------
# Stack alphabet tests
# ---------------------------------------------------------------------------


class TestStackAlphabet:
    def test_get_stack_alphabet(self, pda_anbn):
        sa = pda_anbn.get_stack_alphabet()
        assert "Z" in sa
        assert "A" in sa

    def test_get_stack_alphabet_empty_raises(self):
        pda = PushdownAutomaton.__new__(PushdownAutomaton)
        pda.stack_alphabet = set()
        pda.GRAMMAR = "Context-Free"
        with pytest.raises(ReadError):
            pda.get_stack_alphabet()

    def test_add_duplicate_stack_symbol_raises(self, empty_pda):
        with pytest.raises(AddError):
            empty_pda._add_stack_symbol("Z")  # already present


# ---------------------------------------------------------------------------
# Stack operation tests
# ---------------------------------------------------------------------------


class TestStackOperations:
    def test_push_valid(self, pda_anbn):
        pda_anbn.push("A")
        assert pda_anbn.stack[-1] == "A"

    def test_push_invalid_symbol_raises(self, pda_anbn):
        with pytest.raises(AddError):
            pda_anbn.push("X")  # not in stack alphabet

    def test_pop(self, pda_anbn):
        pda_anbn.push("A")
        top = pda_anbn.pop()
        assert top == "A"

    def test_pop_empty_raises(self):
        pda = PushdownAutomaton(name="p")
        pda.stack = []
        with pytest.raises(RemoveComponentError):
            pda.pop()

    def test_peek(self, pda_anbn):
        pda_anbn.push("A")
        assert pda_anbn.peek() == "A"
        assert pda_anbn.stack[-1] == "A"  # not removed

    def test_peek_empty_raises(self):
        pda = PushdownAutomaton(name="p")
        pda.stack = []
        with pytest.raises(RemoveComponentError):
            pda.peek()

    def test_reset_stack(self, pda_anbn):
        pda_anbn.push("A")
        pda_anbn.push("A")
        pda_anbn.reset_stack()
        assert pda_anbn.stack == ["Z"]


# ---------------------------------------------------------------------------
# Input management tests
# ---------------------------------------------------------------------------


class TestInputManagement:
    def test_set_input_valid(self, pda_anbn):
        pda_anbn.set_input(["a", "b"])
        assert pda_anbn.input_word == ["a", "b"]
        assert pda_anbn.input_pos == 0

    def test_set_input_invalid_symbol_raises(self, pda_anbn):
        with pytest.raises(ReadError):
            pda_anbn.set_input(["a", "x"])

    def test_current_input_within_word(self, pda_anbn):
        pda_anbn.set_input(["a", "b"])
        assert pda_anbn._current_input() == "a"

    def test_current_input_end_of_word(self, pda_anbn):
        pda_anbn.set_input(["a"])
        pda_anbn.input_pos = 1
        assert pda_anbn._current_input() is None


# ---------------------------------------------------------------------------
# Register (state) tests
# ---------------------------------------------------------------------------


class TestRegister:
    def test_set_register_sets_start(self, empty_pda):
        empty_pda.set_register("q0")
        assert empty_pda.register == "q0"
        assert empty_pda.grammar.start == "q0"
        assert "q0" in empty_pda.grammar.states

    def test_set_register_second_call_no_start_change(self, empty_pda):
        empty_pda.set_register("q0")
        empty_pda.set_register("q1")
        assert empty_pda.grammar.start == "q0"  # start doesn't change


# ---------------------------------------------------------------------------
# Transition tests
# ---------------------------------------------------------------------------


class TestTransitions:
    def test_add_transition_valid(self, pda_anbn):
        rules = pda_anbn.get_rules()
        assert ("q0", "a", "Z", "q0", ["A", "Z"]) in rules

    def test_add_transition_duplicate_raises(self, pda_anbn):
        with pytest.raises(AddError):
            pda_anbn.add_transition("q0", "a", "Z", "q0", ["A", "Z"])

    def test_add_transition_invalid_input_symbol_raises(self, pda_anbn):
        with pytest.raises(ReadError):
            pda_anbn.add_transition("q0", "x", "Z", "q0", [])

    def test_add_transition_invalid_stack_top_raises(self, pda_anbn):
        with pytest.raises(AddError):
            pda_anbn.add_transition("q0", "a", "X", "q0", [])

    def test_add_transition_invalid_stack_ops_raises(self, pda_anbn):
        with pytest.raises(AddError):
            pda_anbn.add_transition("q0", "a", "Z", "q0", ["X"])

    def test_add_transition_epsilon_raises(self, pda_anbn):
        with pytest.raises(NotImplementedError):
            pda_anbn.add_transition("q0", None, "Z", "q0", [])

    def test_states_auto_added(self, pda_anbn):
        assert "q1" in pda_anbn.grammar.states
        assert "q2" in pda_anbn.grammar.states


# ---------------------------------------------------------------------------
# Step tests
# ---------------------------------------------------------------------------


class TestStep:
    def test_step_single(self, pda_anbn):
        """One step: read 'a' in q0 with Z on top → push A, Z."""
        pda_anbn.set_input(["a", "b"])
        assert pda_anbn.register == "q0"
        assert pda_anbn.peek() == "Z"
        pda_anbn.step()
        assert pda_anbn.register == "q0"
        assert pda_anbn.peek() == "A"
        assert pda_anbn.input_pos == 1

    def test_step_no_valid_transition_raises(self, pda_anbn):
        """Step with no matching rule raises Exception."""
        pda_anbn.set_input(["b"])  # 'b' with Z on top and in state q0 — no rule
        with pytest.raises(Exception):
            pda_anbn.step()


# ---------------------------------------------------------------------------
# Validation tests — acceptance by empty stack
# ---------------------------------------------------------------------------


class TestValidate:
    @pytest.mark.parametrize(
        "word",
        [
            ["a", "b"],
            ["a", "a", "b", "b"],
            ["a", "a", "a", "b", "b", "b"],
        ],
    )
    def test_accepts_anbn(self, pda_anbn, word):
        assert pda_anbn.validate(word) is True

    @pytest.mark.parametrize(
        "word",
        [
            ["a"],
            ["b"],
            ["a", "b", "b"],
            ["a", "a", "b"],
            ["b", "a"],
            [],
        ],
    )
    def test_rejects_non_anbn(self, pda_anbn, word):
        assert pda_anbn.validate(word) is False

    def test_validate_no_start_raises(self):
        pda = PushdownAutomaton(name="p")
        pda.add_terminals("a")
        with pytest.raises(ValidationError):
            pda.validate(["a"])

    def test_validate_no_terminals_raises(self):
        pda = PushdownAutomaton(name="p")
        pda.set_register("q0")
        with pytest.raises(ValidationError):
            pda.validate([])

    def test_validate_no_rules_raises(self):
        pda = PushdownAutomaton(name="p")
        pda.add_terminals("a")
        pda.set_register("q0")
        with pytest.raises(ValidationError):
            pda.validate(["a"])

    def test_validate_resets_state(self, pda_anbn):
        """validate() leaves the PDA in a clean state for subsequent calls."""
        pda_anbn.validate(["a", "b"])
        result = pda_anbn.validate(["a", "a", "b", "b"])
        assert result is True


# ---------------------------------------------------------------------------
# Tape-based method override tests
# ---------------------------------------------------------------------------


class TestTapeOverrides:
    def test_set_tape_raises(self, empty_pda):
        with pytest.raises(NotImplementedError):
            empty_pda.set_tape([])

    def test_read_raises(self, empty_pda):
        with pytest.raises(NotImplementedError):
            empty_pda.read()

    def test_write_raises(self, empty_pda):
        with pytest.raises(NotImplementedError):
            empty_pda.write("a")

    def test_move_raises(self, empty_pda):
        with pytest.raises(NotImplementedError):
            empty_pda.move("F1")
