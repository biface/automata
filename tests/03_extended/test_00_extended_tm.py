"""
Tests for ExtendedTuringMachine (extended.py).
Uses fixtures from conftest.py (importlib-based).
"""

import pytest


class TestInitialization:

    def test_name(self, etm_instance):
        assert etm_instance.name == "TestETM"

    def test_chomsky_grammar(self, etm_instance):
        assert etm_instance.GRAMMAR == "Recursively Enumerable"

    def test_tape_is_dict(self, etm_instance):
        assert isinstance(etm_instance.tape, dict)

    def test_axes_1(self, etm_instance):
        assert etm_instance.axes == 1

    def test_axes_2(self, etm_2d_instance):
        assert etm_2d_instance.axes == 2

    def test_axes_0_raises_value_error(self, fsm_module):
        with pytest.raises(ValueError, match="at least 1 axis"):
            fsm_module.ExtendedTuringMachine("ETM", axes=0, register="S")

    def test_is_turing_machine(self, fsm_module, etm_instance):
        assert isinstance(etm_instance, fsm_module.TuringMachine)

    def test_same_grammar_as_tm(self, fsm_module):
        tm = fsm_module.TuringMachine("TM", register="S")
        etm = fsm_module.ExtendedTuringMachine("ETM", register="S")
        assert etm.GRAMMAR == tm.GRAMMAR


class TestSetTape:

    def test_1d_tape_loaded(self, etm_instance):
        etm_instance.add_terminals("a", "b")
        etm_instance.set_tape(["a", "b"])
        assert etm_instance.tape[(0,)] == "a"
        assert etm_instance.tape[(1,)] == "b"

    def test_2d_tape_loaded(self, etm_2d_instance):
        etm_2d_instance.add_terminals("a", "b")
        etm_2d_instance.set_tape([["a", "b"], ["b", "a"]])
        assert etm_2d_instance.tape[(0, 0)] == "a"
        assert etm_2d_instance.tape[(1, 1)] == "a"

    def test_unknown_symbol_raises_read_error(self, etm_instance, fsm_module):
        etm_instance.add_terminals("a")
        with pytest.raises(fsm_module.ReadError):
            etm_instance.set_tape(["a", "unknown"])

    def test_custom_location(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"], location=[2])
        assert etm_instance.head == [2]


class TestReadWrite:

    def test_read_loaded_symbol(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        assert etm_instance.read() == "a"

    def test_read_unwritten_cell_returns_blank(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        etm_instance.move("F")
        assert etm_instance.read() == "_"

    def test_read_negative_position_returns_blank(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        etm_instance.move("B")
        assert etm_instance.read() == "_"

    def test_write_negative_position(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        etm_instance.move("B")
        etm_instance.write("z")
        assert etm_instance.tape[(-1,)] == "z"

    def test_write_adds_to_alphabet(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        etm_instance.write("new")
        assert "new" in etm_instance.grammar.alphabet


class TestBidirectionalTape:

    def test_move_to_negative_then_read(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        etm_instance.move("B")
        etm_instance.move("B")
        assert etm_instance.head == [-2]
        assert etm_instance.read() == "_"

    def test_move_far_right_returns_blank(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        for _ in range(100):
            etm_instance.move("F")
        assert etm_instance.read() == "_"

    def test_write_and_read_at_any_position(self, etm_instance):
        etm_instance.add_terminals("a")
        etm_instance.set_tape(["a"])
        for _ in range(5):
            etm_instance.move("B")
        etm_instance.write("x")
        assert etm_instance.read() == "x"
