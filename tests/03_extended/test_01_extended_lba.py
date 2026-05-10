"""
Tests for ExtendedLBA (extended.py).
Uses fixtures from conftest.py (importlib-based).
"""

import pytest


class TestInitialization:

    def test_name(self, elba_instance):
        assert elba_instance.name == "TestELBA"

    def test_chomsky_grammar(self, elba_instance):
        assert elba_instance.GRAMMAR == "Context-Sensitive"

    def test_limits_1d(self, elba_instance):
        assert elba_instance.limits == [10]

    def test_limits_2d(self, elba_2d_instance):
        assert elba_2d_instance.limits == [5, 5]

    def test_tape_is_dict(self, elba_instance):
        assert isinstance(elba_instance.tape, dict)

    def test_tape_size_mismatch_raises_value_error(self, fsm_module):
        with pytest.raises(ValueError, match="1 value"):
            fsm_module.ExtendedLBA("E", tape_size=[5, 5], axes=1, register="S")

    def test_is_extended_tm(self, fsm_module, elba_instance):
        assert isinstance(elba_instance, fsm_module.ExtendedTuringMachine)

    def test_is_not_lba(self, fsm_module, elba_instance):
        assert not isinstance(elba_instance, fsm_module.LinearBoundedAutomaton)


class TestSetTape:

    def test_tape_loaded(self, elba_instance):
        elba_instance.add_terminals("a", "b")
        elba_instance.set_tape(["a", "b"])
        assert elba_instance.tape[(0,)] == "a"
        assert elba_instance.tape[(1,)] == "b"

    def test_content_at_exact_limit(self, fsm_module):
        elba = fsm_module.ExtendedLBA(
            "E", tape_size=[3], axes=1,
            movement={"F": [1], "B": [-1]}, register="S"
        )
        elba.add_terminals("a")
        elba.set_tape(["a", "a", "a"])
        assert len(elba.tape) == 3

    def test_content_exceeds_limit_raises_value_error(self, fsm_module):
        elba = fsm_module.ExtendedLBA(
            "E", tape_size=[3], axes=1,
            movement={"F": [1], "B": [-1]}, register="S"
        )
        elba.add_terminals("a")
        with pytest.raises(ValueError, match="exceeds tape limit"):
            elba.set_tape(["a", "a", "a", "a"])

    def test_2d_tape_loaded(self, elba_2d_instance):
        elba_2d_instance.add_terminals("a", "b")
        elba_2d_instance.set_tape([["a", "b"], ["b", "a"]])
        assert elba_2d_instance.tape[(0, 0)] == "a"

    def test_2d_exceeds_limit_raises_value_error(self, elba_2d_instance):
        elba_2d_instance.add_terminals("a")
        with pytest.raises(ValueError, match="exceeds tape limit"):
            elba_2d_instance.set_tape([["a"] * 6])

    def test_unknown_symbol_raises_read_error(self, elba_instance, fsm_module):
        elba_instance.add_terminals("a")
        with pytest.raises(fsm_module.ReadError):
            elba_instance.set_tape(["a", "unknown"])


class TestBoundsEnforcement:

    def test_read_within_bounds(self, elba_instance):
        elba_instance.add_terminals("a")
        elba_instance.set_tape(["a"])
        assert elba_instance.read() == "a"

    def test_read_at_limit_raises_index_error(self, fsm_module):
        elba = fsm_module.ExtendedLBA(
            "E", tape_size=[3], axes=1,
            movement={"F": [1], "B": [-1]}, register="S"
        )
        elba.add_terminals("a")
        elba.set_tape(["a"])
        for _ in range(3):
            elba.move("F")
        with pytest.raises(IndexError, match="exceeds the tape limit"):
            elba.read()

    def test_write_at_limit_raises_index_error(self, fsm_module):
        elba = fsm_module.ExtendedLBA(
            "E", tape_size=[3], axes=1,
            movement={"F": [1], "B": [-1]}, register="S"
        )
        elba.add_terminals("a")
        elba.set_tape(["a"])
        for _ in range(3):
            elba.move("F")
        with pytest.raises(IndexError):
            elba.write("a")

    def test_negative_position_at_limit_raises_index_error(self, fsm_module):
        elba = fsm_module.ExtendedLBA(
            "E", tape_size=[3], axes=1,
            movement={"F": [1], "B": [-1]}, register="S"
        )
        elba.add_terminals("a")
        elba.set_tape(["a"])
        for _ in range(3):
            elba.move("B")
        with pytest.raises(IndexError):
            elba.read()
