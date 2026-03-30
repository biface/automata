import pytest
from fsm_tools.advanced import Grammar, Automaton
from fsm_tools.exception import ReadError, AddError, RemoveError, ModifyError, RemoveComponentError


class MockAutomaton(Automaton):
    """Mock class for Automaton used for testing."""


@pytest.fixture
def grammar_instance():
    """Fixture to create a default Grammar instance."""
    return Grammar(automaton=MockAutomaton("Test Grammar", 'Context-Sensitive'))


def test_initialization(grammar_instance):
    """Test the initialization of the Grammar class."""
    assert grammar_instance.automaton is not None
    assert grammar_instance.alphabet == set()
    assert grammar_instance.states == set()
    assert grammar_instance.rules == []


def test_get_type(grammar_instance):
    """Test the get_type method."""
    assert grammar_instance.get_type() == 1


def test_reset_alphabet(grammar_instance):
    """Test the reset_alphabet method."""
    grammar_instance.alphabet = {'a', 'b', 'c'}
    grammar_instance.reset_alphabet()
    assert grammar_instance.alphabet == set()


def test_reset_states(grammar_instance):
    """Test the reset_states method."""
    grammar_instance.states = {'S', 'A'}
    grammar_instance.reset_states()
    assert grammar_instance.states == set()


def test_reset_rules(grammar_instance):
    """Test the reset_rules method."""
    grammar_instance.rules = ['S -> A', 'A -> a']
    grammar_instance.reset_rules()
    assert grammar_instance.rules == []


def test_reset(grammar_instance):
    """Test the reset method."""
    grammar_instance.alphabet = {'a', 'b'}
    grammar_instance.states = {'S'}
    grammar_instance.rules = ['S -> a']
    grammar_instance.reset()

    assert grammar_instance.alphabet == set()
    assert grammar_instance.states == set()
    assert grammar_instance.rules == []


def test_alphabet_modifications(grammar_instance):
    """Test adding and removing elements in the alphabet."""
    grammar_instance.alphabet.add('a')
    assert 'a' in grammar_instance.alphabet

    grammar_instance.alphabet.remove('a')
    assert 'a' not in grammar_instance.alphabet


def test_states_modifications(grammar_instance):
    """Test adding and removing elements in the states."""
    grammar_instance.states.add('S')
    assert 'S' in grammar_instance.states

    grammar_instance.states.remove('S')
    assert 'S' not in grammar_instance.states


def test_rules_modifications(grammar_instance):
    """Test adding and removing rules."""
    grammar_instance.rules.append('S -> a')
    assert 'S -> a' in grammar_instance.rules

    grammar_instance.rules.remove('S -> a')
    assert 'S -> a' not in grammar_instance.rules


def test_reset_edge_cases(grammar_instance):
    """Test reset methods when components are already empty."""
    grammar_instance.reset_alphabet()
    assert grammar_instance.alphabet == set()

    grammar_instance.reset_states()
    assert grammar_instance.states == set()

    grammar_instance.reset_rules()
    assert grammar_instance.rules == []