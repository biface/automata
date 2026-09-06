"""
Tests for ExtendedPushdownAutomaton — #66.

Classic example: L = {a^n b^n | n >= 0}, i.e. the same recogniser as
test_07_pushdown_automaton.py's aⁿbⁿ fixture, plus one epsilon-transition
(q0, None, Z, q2, [Z]) accepting n=0 directly. The base PushdownAutomaton
rejects the empty word unconditionally (DD-015's stack-vacuity workaround);
this is exactly the case epsilon-transitions were reserved for (DD-013).
"""

import pytest

from fsm_tools.exception import AddError, ReadError, SearchError, ValidationError
from fsm_tools.extended import ExtendedPushdownAutomaton

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def epda_anbn_with_epsilon():
    """L = {a^n b^n | n >= 0} — epsilon-transition covers n=0."""
    epda = ExtendedPushdownAutomaton(name="anbn-eps", stack_alphabet={"A"}, bottom_symbol="Z")
    epda.add_terminals("a", "b")
    epda.set_register("q0")
    epda.add_non_terminals("q1", "q2")

    epda.add_transition("q0", "a", "Z", "q0", ["A", "Z"])
    epda.add_transition("q0", "a", "A", "q0", ["A", "A"])
    epda.add_transition("q0", "b", "A", "q1", [])
    epda.add_transition("q1", "b", "A", "q1", [])
    epda.add_transition("q1", "b", "Z", "q2", [])
    epda.add_transition("q0", None, "Z", "q2", ["Z"])  # epsilon: accept n=0

    return epda


@pytest.fixture
def empty_epda():
    return ExtendedPushdownAutomaton(name="empty")


# ---------------------------------------------------------------------------
# add_transition — epsilon accepted, everything else unchanged
# ---------------------------------------------------------------------------


class TestAddTransitionEpsilon:
    def test_epsilon_transition_accepted(self, empty_epda):
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.add_transition("q0", None, "Z", "q0", ["Z"])
        assert ("q0", None, "Z", "q0", ["Z"]) in empty_epda.get_rules()

    def test_symbol_transition_still_validated(self, empty_epda):
        empty_epda.set_register("q0")
        with pytest.raises(ReadError):
            empty_epda.add_transition("q0", "x", "Z", "q0", [])  # not in alphabet

    def test_duplicate_epsilon_transition_raises(self, empty_epda):
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.add_transition("q0", None, "Z", "q0", ["Z"])
        with pytest.raises(AddError):
            empty_epda.add_transition("q0", None, "Z", "q0", ["Z"])


# ---------------------------------------------------------------------------
# step() — single-transition semantics, epsilon does not advance input_pos
# ---------------------------------------------------------------------------


class TestStepEpsilon:
    def test_epsilon_preferred_over_symbol_transition(self, empty_epda):
        """Both an epsilon-transition and a symbol-transition are applicable
        from q0 with 'Z' on top — step() takes the epsilon one first."""
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.add_non_terminals("q1")
        empty_epda.add_transition("q0", None, "Z", "q1", ["Z"])
        empty_epda.add_transition("q0", "a", "Z", "q0", ["Z"])
        empty_epda.set_input(["a"])

        empty_epda.step()

        assert empty_epda.register == "q1"
        assert empty_epda.input_pos == 0  # epsilon: no input consumed

    def test_step_no_matching_rule_raises_search_error(self, empty_epda):
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.set_input(["a"])
        with pytest.raises(SearchError, match="No rule"):
            empty_epda.step()

    def test_step_symbol_transition_when_no_epsilon_available(self, empty_epda):
        """No epsilon-transition applicable — step() falls through to the
        symbol-consuming branch and does advance input_pos."""
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.add_non_terminals("q1")
        empty_epda.add_transition("q0", "a", "Z", "q1", ["Z"])
        empty_epda.set_input(["a"])

        empty_epda.step()

        assert empty_epda.register == "q1"
        assert empty_epda.input_pos == 1


class TestAddTransitionValidation:
    def test_invalid_stack_top_raises(self, empty_epda):
        empty_epda.set_register("q0")
        with pytest.raises(AddError):
            empty_epda.add_transition("q0", None, "X", "q0", [])  # "X" not in stack alphabet

    def test_invalid_stack_ops_symbol_raises(self, empty_epda):
        empty_epda.set_register("q0")
        with pytest.raises(AddError):
            empty_epda.add_transition("q0", None, "Z", "q0", ["X"])

    def test_new_states_auto_added(self, empty_epda):
        empty_epda.set_register("q0")
        empty_epda.add_transition("q0", None, "Z", "q9", ["Z"])
        assert "q9" in empty_epda.grammar.states


# ---------------------------------------------------------------------------
# validate() — epsilon-closure via BFS over configurations
# ---------------------------------------------------------------------------


class TestValidateEpsilonClosure:
    @pytest.mark.parametrize(
        "word, expected",
        [
            ([], True),
            (["a", "b"], True),
            (["a", "a", "b", "b"], True),
            (["a", "a", "a", "b", "b", "b"], True),
            (["a"], False),
            (["b"], False),
            (["a", "b", "b"], False),
            (["a", "a", "b"], False),
        ],
    )
    def test_epsilon_anbn(self, epda_anbn_with_epsilon, word, expected):
        assert epda_anbn_with_epsilon.validate(word) is expected

    def test_epsilon_cycle_does_not_infinite_loop(self, empty_epda):
        """A self-looping epsilon-transition must not hang validate()."""
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        empty_epda.add_transition("q0", None, "Z", "q0", ["Z"])  # epsilon self-loop
        assert empty_epda.validate(["a"]) is False

    def test_validate_no_start_raises(self, empty_epda):
        empty_epda.add_terminals("a")
        with pytest.raises(ValidationError):
            empty_epda.validate(["a"])

    def test_validate_no_terminals_raises(self, empty_epda):
        empty_epda.set_register("q0")
        with pytest.raises(ValidationError):
            empty_epda.validate([])

    def test_validate_no_rules_raises(self, empty_epda):
        empty_epda.add_terminals("a")
        empty_epda.set_register("q0")
        with pytest.raises(ValidationError):
            empty_epda.validate(["a"])

    def test_validate_reusable_across_calls(self, epda_anbn_with_epsilon):
        assert epda_anbn_with_epsilon.validate(["a", "b"]) is True
        assert epda_anbn_with_epsilon.validate([]) is True
        assert epda_anbn_with_epsilon.validate(["a"]) is False
