import pytest

from fsm_tools.constants import CHOMSKY_GRAMMARS
from fsm_tools.advanced import Grammar, Automaton
from fsm_tools.exception import ReadError, AddError, RemoveError, ModifyError, RemoveComponentError

@pytest.fixture
def automaton_instance():
    """Fixture to create an Automaton instance."""
    return Automaton(name="TestAutomaton", chomsky="Regular")

@pytest.fixture
def empty_automaton():
    """Fixture for an Automaton without grammar type."""
    return Automaton(name="EmptyAutomaton")

def test_initialization(automaton_instance):
    """Test initialization of Automaton."""
    assert automaton_instance.name == "TestAutomaton"
    assert automaton_instance.GRAMMAR == "Regular"
    assert automaton_instance.TYPE == 3
    assert isinstance(automaton_instance.grammar, Grammar)

def test_invalid_chomsky_type():
    """Test exception raised for invalid Chomsky grammar type."""
    with pytest.raises(KeyError):
        Automaton(name="InvalidAutomaton", chomsky="InvalidType")

def test_get_terminals(automaton_instance):
    """Test retrieving terminal symbols."""
    with pytest.raises(ReadError):
        automaton_instance.get_terminals()
    automaton_instance.add_terminals("a", "b")
    assert automaton_instance.get_terminals() == {"a", "b"}

def test_add_terminals(automaton_instance):
    """Test adding terminal symbols."""
    automaton_instance.add_terminals("x", "y")
    assert automaton_instance.get_terminals() == {"x", "y"}
    with pytest.raises(AddError):
        automaton_instance.add_terminals("x")  # Duplicate terminal

def test_remove_terminals(automaton_instance):
    """Test removing terminal symbols."""
    automaton_instance.add_terminals("a", "b")
    assert "a" in automaton_instance.get_terminals()
    automaton_instance.remove_terminals("a")
    assert "a" not in automaton_instance.get_terminals()
    with pytest.raises(RemoveError):
        automaton_instance.remove_terminals("a")
    automaton_instance.remove_terminals("b")
    with pytest.raises(ReadError):
        automaton_instance.get_terminals()# Non-existent terminal

def test_modify_terminal(automaton_instance):
    """Test modifying terminal symbols."""
    automaton_instance.add_terminals("a")
    automaton_instance.modify_terminal("a", "b")
    assert "a" not in automaton_instance.get_terminals()
    assert "b" in automaton_instance.get_terminals()
    with pytest.raises(ModifyError):
        automaton_instance.modify_terminal("c", "d")  # Non-existent terminal

def test_withdraw_terminal(automaton_instance):
    """Test withdrawing all terminals."""
    automaton_instance.add_terminals("a", "b")
    automaton_instance.withdraw_terminal()
    assert automaton_instance.grammar.alphabet == set()
    with pytest.raises(ReadError):
        automaton_instance.withdraw_terminal()  # Already empty

def test_get_states(automaton_instance):
    """Test retrieving states."""
    automaton_instance.add_non_terminals("S", "A")
    assert automaton_instance.get_states() == {"S", "A"}

def test_add_non_terminals(automaton_instance):
    """Test adding non-terminal symbols."""
    automaton_instance.add_non_terminals("S", "A")
    assert automaton_instance.get_states() == {"S", "A"}
    with pytest.raises(AddError):
        automaton_instance.add_non_terminals("S")  # Duplicate non-terminal

def test_remove_non_terminals(automaton_instance):
    """Test removing non-terminal symbols."""
    automaton_instance.add_non_terminals("S", "T")
    automaton_instance.remove_non_terminals("S")
    assert "S" not in automaton_instance.get_states()
    with pytest.raises(RemoveError):
        automaton_instance.remove_non_terminals("S")  # Non-existent non-terminal

def test_modify_non_terminal(automaton_instance):
    """Test modifying non-terminal symbols."""
    automaton_instance.add_non_terminals("S")
    automaton_instance.modify_non_terminal("S", "A")
    assert "S" not in automaton_instance.get_states()
    assert "A" in automaton_instance.get_states()
    with pytest.raises(ModifyError):
        automaton_instance.modify_non_terminal("B", "C")  # Non-existent non-terminal

def test_withdraw_non_terminal(automaton_instance):
    """Test withdrawing all non-terminals."""
    automaton_instance.add_non_terminals("S", "A")
    automaton_instance.withdraw_non_terminal()
    assert automaton_instance.grammar.states == set()
    with pytest.raises(KeyError):
        automaton_instance.withdraw_non_terminal()  # Already empty

def test_get_rules(automaton_instance):
    """Test retrieving rules."""
    with pytest.raises(ValueError):
        automaton_instance.get_rules()
    automaton_instance.add_rules("S -> A", "A -> a")
    assert automaton_instance.get_rules() == ["S -> A", "A -> a"]

def test_add_rules(automaton_instance):
    """Test adding rules."""
    automaton_instance.add_rules("S -> A")
    assert "S -> A" in automaton_instance.get_rules()

def test_remove_rules(automaton_instance):
    """Test removing rules."""
    automaton_instance.add_rules("S -> A", "A -> a")
    automaton_instance.remove_rules("S -> A")
    assert "S -> A" not in automaton_instance.get_rules()
    with pytest.raises(ValueError):
        automaton_instance.remove_rules("S -> A")  # Non-existent rule

def test_withdraw_rules(automaton_instance):
    """Test withdrawing all rules."""
    automaton_instance.add_rules("S -> A")
    automaton_instance.withdraw_rules()
    assert automaton_instance.grammar.rules == []
    with pytest.raises(ValueError):
        automaton_instance.withdraw_rules()  # Already empty

def test_withdraw_grammar(automaton_instance):
    """Test withdrawing the entire grammar."""
    automaton_instance.add_terminals("a")
    automaton_instance.add_non_terminals("S")
    automaton_instance.add_rules("S -> a")
    automaton_instance.withdraw_grammar()
    assert automaton_instance.grammar.alphabet == set()
    assert automaton_instance.grammar.states == set()
    assert automaton_instance.grammar.rules == []
