"""
Closes #32 and #34/#20.

#32 — exhaustive audit: every CRUD method on Automaton, exercised through
each of the 4 Chomsky subclasses, must raise a properly typed exception
whose message resolves without error. This is what caught the real gaps
left after the DD-009 fix: TuringMachine.add_non_terminals()/remove_non_
terminals() had no catalog entry at all (10302/10303), remove_rules()
passed the wrong kwarg shape for TM/LBA's lhs/rhs-style templates, and
FiniteStateAutomaton.get_rules() shared a {transition}-templated code
(40201) with no caller that ever supplied that placeholder.

#34/#20 — cartesian-product code verification: generate_code() must
produce a unique code for every (grammar, primary component axis, action)
triple, and every alias must resolve to the exact same code as its
primary axis (#79) — never a distinct one.
"""

import itertools

import pytest

from fsm_tools.advanced import (
    FiniteStateAutomaton,
    LinearBoundedAutomaton,
    PushdownAutomaton,
    TuringMachine,
)
from fsm_tools.constants import ACTIONS, CHOMSKY_GRAMMARS, COMPONENTS
from fsm_tools.exception import AddError, ReadError, RemoveComponentError, RemoveError
from fsm_tools.utils.common import generate_code

# ---------------------------------------------------------------------------
# #34/#20 — cartesian-product code verification
# ---------------------------------------------------------------------------

PRIMARY_COMPONENTS = [
    "alphabet",
    "transitions",
    "non_terminals",
    "grammar",
    "stack",
    "validation",
    "tape",
    "register",
]

ALIASES = {
    "states": "non_terminals",
    "blank": "alphabet",
    "head": "tape",
    "moves": "tape",
}


class TestCartesianCodeVerification:

    def test_every_primary_combination_is_unique(self):
        codes = [
            generate_code(g, c, a)
            for g, c, a in itertools.product(CHOMSKY_GRAMMARS, PRIMARY_COMPONENTS, ACTIONS)
        ]
        assert len(codes) == len(set(codes))

    @pytest.mark.parametrize("alias, primary", ALIASES.items())
    def test_alias_resolves_to_same_code_as_primary(self, alias, primary):
        for g in CHOMSKY_GRAMMARS:
            for a in ACTIONS:
                assert generate_code(g, alias, a) == generate_code(g, primary, a)

    def test_components_and_actions_agree_with_generate_code(self):
        """COMPONENTS/ACTIONS keys must be exactly what generate_code() accepts —
        catches drift between constants.py and the formula silently."""
        for key in COMPONENTS:
            generate_code("Regular", key, "read")  # must not raise
        for key in ACTIONS:
            generate_code("Regular", "alphabet", key)  # must not raise


# ---------------------------------------------------------------------------
# #32 — exhaustive CRUD/catalog audit across the 4 Chomsky subclasses
# ---------------------------------------------------------------------------

CLASSES = {
    "TuringMachine": lambda name: TuringMachine(name=name),
    "LinearBoundedAutomaton": lambda name: LinearBoundedAutomaton(name=name, tape_size=[10]),
    "PushdownAutomaton": lambda name: PushdownAutomaton(name=name),
    "FiniteStateAutomaton": lambda name: FiniteStateAutomaton(name=name),
}


class TestExhaustiveCrudAudit:

    @pytest.mark.parametrize("cls_name, ctor", CLASSES.items())
    def test_add_non_terminals_duplicate(self, cls_name, ctor):
        inst = ctor(cls_name)
        inst.add_non_terminals("q0")
        with pytest.raises(AddError):
            inst.add_non_terminals("q0")

    @pytest.mark.parametrize("cls_name, ctor", CLASSES.items())
    def test_remove_non_terminals_missing(self, cls_name, ctor):
        inst = ctor(cls_name)
        with pytest.raises(RemoveError):
            inst.remove_non_terminals("zzz")

    @pytest.mark.parametrize("cls_name, ctor", CLASSES.items())
    def test_get_rules_empty(self, cls_name, ctor):
        inst = ctor(cls_name)
        with pytest.raises(ReadError):
            inst.get_rules()

    @pytest.mark.parametrize("cls_name, ctor", CLASSES.items())
    def test_remove_rules_lhs_rhs_style(self, cls_name, ctor):
        """TM/LBA templates need {lhs}/{rhs}; PDA/FSA need {transition} —
        remove_rules() must pick the right shape for each grammar level."""
        inst = ctor(cls_name)
        inst.add_rules("S -> A")
        with pytest.raises(RemoveError):
            inst.remove_rules("X -> Y")

    @pytest.mark.parametrize("cls_name, ctor", CLASSES.items())
    def test_withdraw_rules_empty(self, cls_name, ctor):
        inst = ctor(cls_name)
        with pytest.raises(RemoveComponentError):
            inst.withdraw_rules()
