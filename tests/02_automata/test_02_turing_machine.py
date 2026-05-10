"""
Tests for TuringMachine (advanced.py) — #25 coverage target ≥ 80%.
Uses fixtures from conftest.py (importlib-based).
"""

import pytest


class TestInitialization:

    def test_name(self, tm_instance):
        assert tm_instance.name == "TestTM"

    def test_axes(self, tm_instance):
        assert tm_instance.axes == 1

    def test_blank_symbol(self, tm_instance):
        assert tm_instance.blank == "_"

    def test_head_initial_position(self, tm_instance):
        assert tm_instance.head == [0]

    def test_register(self, tm_instance):
        assert tm_instance.register == "S"

    def test_validation_states(self, tm_instance):
        assert tm_instance.validation["accept"] == "OK"
        assert tm_instance.validation["reject"] == "nOK"

    def test_blank_in_alphabet(self, tm_instance):
        assert "_" in tm_instance.grammar.alphabet

    def test_default_moves_generated(self, fsm_module):
        """Default moves F1/B1 are generated when movement=None."""
        tm = fsm_module.TuringMachine("TM", register="S")
        assert "F1" in tm.moves
        assert "B1" in tm.moves

    def test_custom_moves(self, tm_instance):
        assert tm_instance.moves == {"F": [1], "B": [-1]}


class TestValidateAxes:

    def test_axes_1_accepted(self, fsm_module):
        tm = fsm_module.TuringMachine("TM", axes=1, register="S")
        assert tm.axes == 1

    def test_axes_2_raises_value_error(self, fsm_module):
        with pytest.raises(ValueError, match="axes=2"):
            fsm_module.TuringMachine("TM", axes=2, register="S")

    def test_axes_0_raises_value_error(self, fsm_module):
        with pytest.raises(ValueError, match="axes=0"):
            fsm_module.TuringMachine("TM", axes=0, register="S")


class TestExtendTape:

    def test_extends_right_on_read(self, tm_instance):
        """Tape extends to the right when head moves beyond initial content."""
        tm_instance.add_terminals("a")
        tm_instance.set_tape(["a"])
        tm_instance.move("F")
        assert tm_instance.read() == "_"

    def test_extended_cells_are_blank(self, tm_instance):
        tm_instance.add_terminals("a")
        tm_instance.set_tape(["a"])
        for _ in range(5):
            tm_instance.move("F")
        assert tm_instance.read() == "_"

    def test_negative_position_raises_index_error(self, tm_instance):
        tm_instance.add_terminals("a")
        tm_instance.set_tape(["a"])
        tm_instance.move("B")
        with pytest.raises(IndexError, match="position 0"):
            tm_instance.read()

    def test_tape_length_grows(self, tm_instance):
        tm_instance.add_terminals("a")
        tm_instance.set_tape(["a"])
        initial_len = len(tm_instance.tape)
        for _ in range(3):
            tm_instance.move("F")
        tm_instance.read()
        assert len(tm_instance.tape) > initial_len


class TestSetTape:

    def test_tape_content(self, tm_with_tape):
        assert tm_with_tape.tape == ["a", "b", "c"]

    def test_head_at_origin(self, tm_with_tape):
        assert tm_with_tape.head == [0]

    def test_custom_location(self, tm_instance):
        tm_instance.add_terminals("a", "b")
        tm_instance.set_tape(["a", "b"], location=[1])
        assert tm_instance.head == [1]

    def test_unknown_symbol_raises_read_error(self, tm_instance, fsm_module):
        tm_instance.add_terminals("a")
        with pytest.raises(fsm_module.ReadError):
            tm_instance.set_tape(["a", "unknown"])


class TestSetRegister:

    def test_register_updated(self, tm_instance):
        tm_instance.set_register("Q1")
        assert tm_instance.register == "Q1"

    def test_new_register_added_to_states(self, tm_instance):
        tm_instance.set_register("NEW")
        assert "NEW" in tm_instance.grammar.states

    def test_existing_register_not_duplicated(self, tm_instance):
        tm_instance.set_register("S")
        count = sum(1 for s in tm_instance.grammar.states if s == "S")
        assert count == 1

    def test_grammar_start_set_on_first_call(self, fsm_module):
        tm = fsm_module.TuringMachine("TM", register="")
        tm.set_register("Q0")
        assert tm.grammar.start == "Q0"

    def test_grammar_start_not_overwritten(self, fsm_module):
        tm = fsm_module.TuringMachine("TM", register="")
        tm.set_register("Q0")
        tm.set_register("Q1")
        assert tm.grammar.start == "Q0"


class TestSetMoves:

    def test_moves_replaced(self, tm_instance):
        tm_instance.set_moves(L=[-1], R=[1])
        assert tm_instance.moves == {"L": [-1], "R": [1]}


class TestRead:

    def test_reads_first_symbol(self, tm_with_tape):
        assert tm_with_tape.read() == "a"

    def test_reads_after_move(self, tm_with_tape):
        tm_with_tape.move("F")
        assert tm_with_tape.read() == "b"


class TestWrite:

    def test_writes_symbol(self, tm_with_tape):
        tm_with_tape.write("x")
        assert tm_with_tape.tape[0] == "x"

    def test_new_symbol_added_to_alphabet(self, tm_with_tape):
        tm_with_tape.write("z")
        assert "z" in tm_with_tape.grammar.alphabet

    def test_existing_symbol_not_duplicated_in_alphabet(self, tm_with_tape):
        tm_with_tape.write("a")
        count = sum(1 for s in tm_with_tape.grammar.alphabet if s == "a")
        assert count == 1


class TestMove:

    def test_move_forward(self, tm_with_tape):
        tm_with_tape.move("F")
        assert tm_with_tape.head == [1]

    def test_move_backward(self, tm_with_tape):
        tm_with_tape.move("F")
        tm_with_tape.move("B")
        assert tm_with_tape.head == [0]

    def test_invalid_direction_raises_value_error(self, tm_with_tape):
        with pytest.raises(ValueError, match="Invalid direction"):
            tm_with_tape.move("X")


class TestAddTransition:

    def test_valid_transition_added(self, tm_instance):
        tm_instance.add_terminals("a")
        tm_instance.add_transition("S", "a", "S1", "b", "F")
        assert ("S", "a", "S1", "b", "F") in tm_instance.get_rules()

    def test_unknown_symbol_raises_read_error(self, tm_instance, fsm_module):
        with pytest.raises(fsm_module.ReadError):
            tm_instance.add_transition("S", "unknown", "S1", "b", "F")

    def test_invalid_direction_raises_value_error(self, tm_instance):
        tm_instance.add_terminals("a")
        with pytest.raises(ValueError, match="Invalid move direction"):
            tm_instance.add_transition("S", "a", "S1", "b", "INVALID")

    def test_new_states_added(self, tm_instance):
        tm_instance.add_terminals("a")
        tm_instance.add_transition("S", "a", "S1", "b", "F")
        assert "S1" in tm_instance.grammar.states


class TestStep:

    def test_step_writes_and_moves(self, tm_instance):
        tm_instance.add_terminals("a", "c")
        tm_instance.add_transition("S", "a", "S1", "b", "F")
        tm_instance.set_tape(["a", "c"])
        tm_instance.set_register("S")
        tm_instance.step()
        assert tm_instance.register == "S1"
        assert tm_instance.tape[0] == "b"
        assert tm_instance.head == [1]

    def test_step_no_transition_raises(self, tm_instance):
        tm_instance.add_terminals("x")
        tm_instance.set_tape(["x"])
        with pytest.raises(Exception, match="No valid transition"):
            tm_instance.step()

    def test_full_run_symbol_replacement(self, fsm_module):
        """Replace all 'a' with 'b' until blank: aaa → bbb."""
        tm = fsm_module.TuringMachine(
            "Replace", blank_symbol="_",
            movement={"R": [1]}, register="q0"
        )
        tm.add_terminals("a", "b")
        tm.add_transition("q0", "a", "q0", "b", "R")
        tm.add_transition("q0", "_", "qOK", "_", "R")
        tm.set_tape(["a", "a", "a"])
        tm.set_register("q0")
        steps = 0
        while tm.register not in ("qOK", "nOK") and steps < 10:
            tm.step()
            steps += 1
        assert tm.tape[0] == "b"
        assert tm.tape[1] == "b"
        assert tm.tape[2] == "b"
        assert tm.register == "qOK"
