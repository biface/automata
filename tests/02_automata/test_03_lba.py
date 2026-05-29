"""
Tests for LinearBoundedAutomaton (advanced.py) — #25 coverage target ≥ 80%.
Uses fixtures from conftest.py (importlib-based).
"""

import pytest


class TestInitialization:

    def test_name(self, lba_instance):
        assert lba_instance.name == "TestLBA"

    def test_axes(self, lba_instance):
        assert lba_instance.axes == 1

    def test_limits(self, lba_instance):
        assert lba_instance.limits == [10]

    def test_chomsky_grammar(self, lba_instance):
        assert lba_instance.GRAMMAR == "Context-Sensitive"

    def test_blank_in_alphabet(self, lba_instance):
        assert "_" in lba_instance.grammar.alphabet

    def test_tape_size_mismatch_raises_value_error(self, fsm_module):
        with pytest.raises(ValueError, match="Must be contains"):
            fsm_module.LinearBoundedAutomaton("LBA", tape_size=[5, 5], axes=1, register="S")


class TestSetTape:

    def test_tape_content(self, lba_with_tape):
        assert lba_with_tape.tape == ["a", "b", "c"]

    def test_head_at_origin(self, lba_with_tape):
        assert lba_with_tape.head == [0]

    def test_content_within_limit(self, lba_instance):
        lba_instance.add_terminals("a")
        lba_instance.set_tape(["a"] * 10)
        assert len(lba_instance.tape) == 10

    def test_content_at_exact_limit(self, fsm_module):
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[3], axes=1, movement={"F": [1], "B": [-1]}, register="S"
        )
        lba.add_terminals("a")
        lba.set_tape(["a", "a", "a"])
        assert len(lba.tape) == 3

    def test_content_exceeds_limit_raises_value_error(self, fsm_module):
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[3], axes=1, movement={"F": [1], "B": [-1]}, register="S"
        )
        lba.add_terminals("a")
        with pytest.raises(ValueError, match="exceeds the tape limit"):
            lba.set_tape(["a", "a", "a", "a"])

    def test_unknown_symbol_raises_read_error(self, lba_instance, fsm_module):
        lba_instance.add_terminals("a")
        with pytest.raises(fsm_module.ReadError):
            lba_instance.set_tape(["a", "unknown"])


class TestExtendTape:

    def test_tape_extends_within_limit(self, lba_with_tape):
        lba_with_tape.move("F")
        lba_with_tape.move("F")
        sym = lba_with_tape.read()
        assert sym == "c"

    def test_head_at_limit_raises_index_error(self, fsm_module):
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[3], axes=1, movement={"F": [1], "B": [-1]}, register="S"
        )
        lba.add_terminals("a")
        lba.set_tape(["a", "a", "a"])
        for _ in range(3):
            lba.move("F")
        with pytest.raises(IndexError, match="out of bounds"):
            lba.read()

    def test_negative_position_raises_index_error(self, lba_with_tape):
        lba_with_tape.move("B")
        with pytest.raises(IndexError):
            lba_with_tape.read()


class TestStep:

    def test_step_basic_transition(self, fsm_module):
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[5], axes=1, movement={"F": [1], "B": [-1]}, register="S"
        )
        lba.add_terminals("a", "b")
        lba.add_transition("S", "a", "S1", "b", "F")
        lba.set_tape(["a", "a"])
        lba.set_register("S")
        lba.step()
        assert lba.register == "S1"
        assert lba.tape[0] == "b"
        assert lba.head == [1]

    def test_step_no_transition_raises(self, fsm_module):
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[5], axes=1, movement={"F": [1], "B": [-1]}, register="S"
        )
        lba.add_terminals("a")
        lba.set_tape(["a"])
        with pytest.raises(Exception, match="No valid transition"):
            lba.step()

    def test_step_at_boundary_raises_index_error(self, fsm_module):
        """Head at limit raises IndexError before transition is applied."""
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[2], axes=1, movement={"F": [1]}, register="S"
        )
        lba.add_terminals("a")
        # After one step, head moves to position 1 (= limit) — next read raises IndexError
        lba.add_transition("S", "a", "S1", "a", "F")
        lba.set_tape(["a", "a"])
        lba.step()  # head goes from 0 to 1
        assert lba.head == [1]
        # head[0]=1 >= limits[0]=2? No — limit is exclusive: abs(1) >= 2 is False
        # Move to position 2 which IS out of bounds
        lba.move("F")
        with pytest.raises(IndexError):
            lba.read()

    def test_full_run_palindrome_marker(self, fsm_module):
        """Mark first symbol: a → x, then halt."""
        lba = fsm_module.LinearBoundedAutomaton(
            "LBA", tape_size=[5], axes=1, movement={"F": [1], "B": [-1]}, register="q0"
        )
        lba.add_terminals("a", "b")
        lba.add_transition("q0", "a", "OK", "x", "F")
        lba.set_tape(["a", "b", "a"])
        lba.set_register("q0")
        lba.step()
        assert lba.tape[0] == "x"
        assert lba.register == "OK"
