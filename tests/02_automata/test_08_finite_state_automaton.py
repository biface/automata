"""
Tests for FiniteStateAutomaton (Type 3 — Regular).

Classic example: turnstile automaton (mirrors the former lightweight `FSM`
tests, removed in DD-001).

Grammar:
    - Input alphabet: {coin, push}
    - States: {locked, unlocked}
    - Start state: locked
    - Accepting states: {locked}  — the turnstile is "at rest" only when locked
    - Acceptance: after consuming the word, current state is accepting

Transitions:
    (locked,   coin, unlocked)  — inserting a coin unlocks the turnstile
    (locked,   push, locked)    — pushing while locked has no effect
    (unlocked, push, locked)    — pushing while unlocked locks it back
    (unlocked, coin, unlocked)  — inserting a coin while already unlocked has no effect
"""

import pytest

from fsm_tools import FiniteStateAutomaton, LinearBoundedAutomaton, PushdownAutomaton
from fsm_tools.exception import (
    AddError,
    ReadError,
    RemoveError,
    SearchError,
    ValidationError,
    WriteError,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def turnstile_fsa():
    """Turnstile DFA — accepts any word that ends in state 'locked'."""
    fsa = FiniteStateAutomaton(name="turnstile", accepting_states={"locked"})
    fsa.add_terminals("coin", "push")
    fsa.set_register("locked")
    fsa.add_non_terminals("unlocked")

    fsa.add_transition("locked", "coin", "unlocked")
    fsa.add_transition("locked", "push", "locked")
    fsa.add_transition("unlocked", "push", "locked")
    fsa.add_transition("unlocked", "coin", "unlocked")

    return fsa


@pytest.fixture
def empty_fsa():
    """Minimal unconfigured FSA."""
    return FiniteStateAutomaton(name="empty")


# ---------------------------------------------------------------------------
# Initialisation tests
# ---------------------------------------------------------------------------


class TestFiniteStateAutomatonInit:
    def test_init_default(self, empty_fsa):
        """Default init sets GRAMMAR, TYPE, and an empty accepting_states set."""
        assert empty_fsa.GRAMMAR == "Regular"
        assert empty_fsa.TYPE == 3
        assert empty_fsa.accepting_states == set()
        assert empty_fsa.register == ""
        assert empty_fsa.input_word == []
        assert empty_fsa.input_pos == 0

    def test_init_with_accepting_states(self):
        fsa = FiniteStateAutomaton(name="x", accepting_states={"a", "b"})
        assert fsa.accepting_states == {"a", "b"}
        assert "a" in fsa.get_states()
        assert "b" in fsa.get_states()

    def test_formal_hierarchy_membership(self, empty_fsa):
        """FSA preserves formal membership in the Chomsky hierarchy (DD-015)."""
        assert isinstance(empty_fsa, PushdownAutomaton)
        assert isinstance(empty_fsa, LinearBoundedAutomaton)


# ---------------------------------------------------------------------------
# Accepting states management
# ---------------------------------------------------------------------------


class TestAcceptingStates:
    def test_add_accepting_state(self, empty_fsa):
        empty_fsa.add_accepting_state("q0")
        assert "q0" in empty_fsa.accepting_states
        assert "q0" in empty_fsa.get_states()

    def test_remove_accepting_state(self, turnstile_fsa):
        turnstile_fsa.remove_accepting_state("locked")
        assert "locked" not in turnstile_fsa.accepting_states

    def test_remove_accepting_state_not_accepting_raises(self, turnstile_fsa):
        with pytest.raises(RemoveError):
            turnstile_fsa.remove_accepting_state("unlocked")

    def test_get_accepting_states_empty_raises(self, empty_fsa):
        with pytest.raises(ReadError):
            empty_fsa.get_accepting_states()

    def test_get_accepting_states(self, turnstile_fsa):
        assert turnstile_fsa.get_accepting_states() == {"locked"}


# ---------------------------------------------------------------------------
# Transition management
# ---------------------------------------------------------------------------


class TestAddTransition:
    def test_add_transition_unknown_symbol_raises(self, empty_fsa):
        empty_fsa.add_terminals("a")
        with pytest.raises(ReadError):
            empty_fsa.add_transition("q0", "b", "q1")

    def test_add_transition_creates_states(self, empty_fsa):
        empty_fsa.add_terminals("a")
        empty_fsa.add_transition("q0", "a", "q1")
        assert "q0" in empty_fsa.get_states()
        assert "q1" in empty_fsa.get_states()

    def test_add_transition_duplicate_pair_raises(self, empty_fsa):
        """Determinism: a second rule for the same (state, symbol) is rejected,
        even if it targets a different state."""
        empty_fsa.add_terminals("a")
        empty_fsa.add_transition("q0", "a", "q1")
        with pytest.raises(AddError):
            empty_fsa.add_transition("q0", "a", "q2")


# ---------------------------------------------------------------------------
# step()
# ---------------------------------------------------------------------------


class TestStep:
    def test_step_advances_state_and_position(self, turnstile_fsa):
        turnstile_fsa.set_input(["coin"])
        turnstile_fsa.register = "locked"
        turnstile_fsa.step()
        assert turnstile_fsa.register == "unlocked"
        assert turnstile_fsa.input_pos == 1

    def test_step_no_input_raises(self, turnstile_fsa):
        turnstile_fsa.set_input([])
        turnstile_fsa.register = "locked"
        with pytest.raises(WriteError, match="No input symbol remains"):
            turnstile_fsa.step()

    def test_step_no_matching_transition_raises(self, empty_fsa):
        empty_fsa.add_terminals("a")
        empty_fsa.set_input(["a"])
        empty_fsa.register = "q0"
        with pytest.raises(SearchError, match="No transition matches"):
            empty_fsa.step()


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------


class TestValidate:
    def test_validate_not_configured_raises(self, empty_fsa):
        with pytest.raises(ValidationError):
            empty_fsa.validate(["a"])

    def test_validate_no_alphabet_raises(self, empty_fsa):
        empty_fsa.set_register("q0")
        with pytest.raises(ValidationError):
            empty_fsa.validate(["a"])

    def test_validate_no_transitions_raises(self, empty_fsa):
        empty_fsa.set_register("q0")
        empty_fsa.add_terminals("a")
        with pytest.raises(ValidationError):
            empty_fsa.validate(["a"])

    def test_validate_no_accepting_state_raises(self, empty_fsa):
        empty_fsa.set_register("q0")
        empty_fsa.add_terminals("a")
        empty_fsa.add_transition("q0", "a", "q1")
        with pytest.raises(ValidationError):
            empty_fsa.validate(["a"])

    def test_validate_accepts_empty_word_when_start_is_accepting(self, turnstile_fsa):
        """Standard DFA rule — diverges from PDA (see class docstring / DD-015)."""
        assert turnstile_fsa.validate([]) is True

    def test_validate_rejects_empty_word_when_start_is_not_accepting(self):
        fsa = FiniteStateAutomaton(name="x", accepting_states={"q1"})
        fsa.add_terminals("a")
        fsa.set_register("q0")
        fsa.add_transition("q0", "a", "q1")
        assert fsa.validate([]) is False

    def test_validate_accepts_word_ending_in_locked(self, turnstile_fsa):
        assert turnstile_fsa.validate(["coin", "push"]) is True
        assert turnstile_fsa.validate(["coin", "coin", "push"]) is True

    def test_validate_rejects_word_ending_in_unlocked(self, turnstile_fsa):
        assert turnstile_fsa.validate(["coin"]) is False

    def test_validate_rejects_on_blocked_transition_mid_word(self):
        """Partial transition function: no rule for (state, symbol) mid-word
        blocks the computation — validate() must catch this and return False,
        not propagate the exception (DD-015 rejection model)."""
        fsa = FiniteStateAutomaton(name="partial", accepting_states={"q1"})
        fsa.add_terminals("a", "b")
        fsa.set_register("q0")
        fsa.add_transition("q0", "a", "q1")
        # No rule for (q1, "b") — the word "ab" gets stuck after the first step.
        assert fsa.validate(["a", "b"]) is False

    def test_validate_rejects_on_unknown_symbol(self, turnstile_fsa):
        with pytest.raises(ReadError):
            turnstile_fsa.validate(["jump"])

    def test_validate_resets_state_between_calls(self, turnstile_fsa):
        assert turnstile_fsa.validate(["coin"]) is False
        assert turnstile_fsa.validate([]) is True

    def test_validate_conflicting_transition_raises(self, turnstile_fsa):
        """Defense in depth: add_transition() already forbids this (DD-015's
        determinism guarantee), so this only fires if grammar.rules is
        manipulated directly, bypassing the public API."""
        turnstile_fsa.grammar.rules.append(("locked", "coin", "locked"))
        with pytest.raises(ValidationError, match="conflicting transition"):
            turnstile_fsa.validate(["coin"])

    def test_validate_unreachable_state_raises(self, turnstile_fsa):
        """Defense in depth: every state normally reaches the graph through
        add_transition()/add_non_terminals(), so this only fires if
        grammar.states is manipulated directly."""
        turnstile_fsa.add_non_terminals("island")
        with pytest.raises(ValidationError, match="unreachable"):
            turnstile_fsa.validate(["coin"])


# ---------------------------------------------------------------------------
# Overridden stack methods (inherited from PushdownAutomaton) must be closed
# ---------------------------------------------------------------------------


class TestStackMethodsClosed:
    def test_push_raises(self, empty_fsa):
        with pytest.raises(NotImplementedError):
            empty_fsa.push("X")

    def test_pop_raises(self, empty_fsa):
        with pytest.raises(NotImplementedError):
            empty_fsa.pop()

    def test_peek_raises(self, empty_fsa):
        with pytest.raises(NotImplementedError):
            empty_fsa.peek()

    def test_reset_stack_raises(self, empty_fsa):
        with pytest.raises(NotImplementedError):
            empty_fsa.reset_stack()

    def test_set_input_still_works(self, empty_fsa):
        """set_input() is NOT stack-related — must remain usable (DD-015 fix)."""
        empty_fsa.add_terminals("a")
        empty_fsa.set_input(["a"])
        assert empty_fsa.input_word == ["a"]
        assert empty_fsa.input_pos == 0

    def test_tape_methods_still_closed(self, empty_fsa):
        """Inherited unchanged from PushdownAutomaton — no tape at any level."""
        with pytest.raises(NotImplementedError):
            empty_fsa.set_tape(["a"])
        with pytest.raises(NotImplementedError):
            empty_fsa.read()
        with pytest.raises(NotImplementedError):
            empty_fsa.write("a")
        with pytest.raises(NotImplementedError):
            empty_fsa.move("R")
