import pytest
from fsm_tools.advanced import TuringMachine
from fsm_tools.exception import ReadError

@pytest.fixture
def turing_machine_instance():
    """Fixture to create a Turing Machine instance."""
    return TuringMachine(name="TestTM", axes=1, blank_symbol="_", movement={"F": [1], "B": [-1]}, register="S", accept="OK", reject="nOK")

def test_initialization(turing_machine_instance):
    """Test initialization of the Turing Machine."""
    assert turing_machine_instance.name == "TestTM"
    assert turing_machine_instance.axes == 1
    assert turing_machine_instance.blank == "_"
    assert turing_machine_instance.head == [0]
    assert turing_machine_instance.register == "S"
    assert turing_machine_instance.validation["accept"] == "OK"
    assert turing_machine_instance.validation["reject"] == "nOK"

def test_set_tape(turing_machine_instance):
    """Test setting the tape for the Turing Machine."""
    turing_machine_instance.add_terminals("a","b","c")
    turing_machine_instance.set_tape(["a", "b", "c"])
    assert turing_machine_instance.tape == ["a", "b", "c"]
    assert turing_machine_instance.head == [0]

    with pytest.raises(ReadError):
        turing_machine_instance.set_tape(["a", "unknown"])  # "unknown" is not in the alphabet

def test_set_register(turing_machine_instance):
    """Test setting the register for the Turing Machine."""
    turing_machine_instance.set_register("NEW_STATE")
    assert turing_machine_instance.register == "NEW_STATE"

def test_set_moves(turing_machine_instance):
    """Test setting moves for the Turing Machine."""
    turing_machine_instance.set_moves(L=[-1], R=[1])
    assert turing_machine_instance.moves == {"L": [-1], "R": [1]}

def test_read(turing_machine_instance):
    """Test reading from the tape."""
    turing_machine_instance.add_terminals("x","y","z")
    turing_machine_instance.set_tape(["x", "y", "z"])
    assert turing_machine_instance.read() == "x"

def test_write(turing_machine_instance):
    """Test writing to the tape."""
    turing_machine_instance.add_terminals("a", "b", "c")
    turing_machine_instance.set_tape(["a", "b", "c"])
    turing_machine_instance.write("x")
    assert turing_machine_instance.tape[0] == "x"


def test_add_transition(turing_machine_instance):
    """Test adding a transition rule."""
    turing_machine_instance.add_terminals("a")
    turing_machine_instance.add_transition("S", "a", "S1", "b", "F")
    assert ("S", "a", "S1", "b", "F") in turing_machine_instance.get_rules()

    with pytest.raises(ReadError):
        turing_machine_instance.add_transition("S", "unknown", "S1", "b", "F")

    with pytest.raises(ValueError):
        turing_machine_instance.add_transition("S", "a", "S1", "b", "InvalidDirection")

def test_step(turing_machine_instance):
    """Test a single step of the Turing Machine."""
    turing_machine_instance.add_terminals("a", "c")
    turing_machine_instance.add_transition("S", "a", "S1", "b", "F")
    turing_machine_instance.set_tape(["a", "c"])
    turing_machine_instance.set_register("S")
    turing_machine_instance.step()

    assert turing_machine_instance.register == "S1"
    assert turing_machine_instance.tape[0] == "b"
    assert turing_machine_instance.head == [1]

def test_no_valid_transition(turing_machine_instance):
    """Test exception raised when no valid transition is found."""
    turing_machine_instance.add_terminals("x", "y", "z")
    turing_machine_instance.set_tape(["x", "y", "z"])
    with pytest.raises(Exception):
        turing_machine_instance.step()  # No transitions defined
