"""
This Python implementation focuses on the formalization of automata, designed to adhere to Chomsky’s grammar
hierarchy. The code implements different types of automata corresponding to the levels of formal languages:
**Deterministic Finite Automata (DFA)** for regular languages, **Pushdown Automata (PDA)** for context-free languages,
**Linear Bounded Automata (LBA)** for context-sensitive languages, and **Turing Machines (TM)** for recursive
languages. The goal is to provide a flexible and modular approach for processing, simulating, and transforming these
automata.

By implementing this, we can explore how automata relate to formal language theory and the classification of languages
from regular to recursively enumerable. This tool can be expanded for educational purposes or used as a basis for
building more complex compilers or language processors.
"""
from __future__ import annotations
from .constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS
from .exception import ReadError, AddError, RemoveError, ModifyError, ValidationError, SearchError, RemoveComponentError

class Grammar:
    """
    Represents a formal grammar and provides a structure for defining the components
    and rules used for language generation or recognition.

    The grammar consists of the following key components:

    Attributes:
        alphabet (set): The set of terminal symbols (the alphabet) used in the grammar.
        states (set): The set of non-terminal symbols that define the recursive structure of the grammar.
        rules (list): A list of production rules, possibly nested, that define the transformations between non-terminals and terminals.
        automaton (Automaton): The automaton that processes the grammar and validates or generates strings.

    Methods:
        __init__(self, alphabet, states, rules, automaton):
            Initializes the Grammar with a given alphabet, set of states, production rules,
            and an automaton to process the grammar.
    """

    def __init__(self, automaton: Automaton = None):
        """
        Initializes the Grammar class with the components necessary for language recognition or generation.

        :param automaton: The automaton that processes the grammar and validates or generates strings.
        :type automaton: Automaton
        """
        self.automaton = automaton
        self.alphabet = set()
        self.states = set()
        self.rules = []

    def get_type(self):
        return self.automaton.TYPE

class Automaton:
    """
    Represents the base class for automata, providing a structure for automata that process
    formal grammars. This class serves as the foundation for specific types of automata, such as
    DFA, PDA, LBA, or TM, that can be used to recognize or generate strings based on the rules
    of a given grammar.

    Attributes:
        GRAMMAR (str): Reference to Chomsky grammar hierarchy.
        TYPE (int): Reference to Chomsky grammar hierarchy type.
        name (str): The name of the automaton. This can be used to identify different types of automata.
        grammar (Grammar): An empty Grammar object initialized as part of the automaton. The grammar can
                           be populated later with terminals, non-terminals, and rules.

    Methods:
        __init__(self, name):
            Initializes the Automaton with a given name and an empty Grammar object.
    """

    GRAMMAR:str = ""
    TYPE:int = 99

    def __init__(self, name: str = ""):
        self.name = name
        self.grammar = Grammar(self)


class TuringMachine(Automaton):

    GRAMMAR = "Recursively Enumerable"
    TYPE = CHOMSKY_GRAMMARS[GRAMMAR] - 1

    def add_terminal(self, symbol):
        """
        This method adds a new terminal to the grammar.

        :param symbol: The symbol to add to the grammar.
        :type symbol: str
        :return: None
        :rtype: None
        :raise AddError: If the symbol cannot be added to the grammar.
        """
        if symbol in self.grammar.alphabet or symbol in self.grammar.states:
            raise AddError(self.GRAMMAR, "alphabet", symbol=str(symbol))

        self.grammar.alphabet.add(symbol)

    def remove_terminal(self, symbol):
        """
        This method removes a terminal from the grammar.

        :param symbol: The symbol to remove from the grammar.
        :type symbol: str
        :return: None
        :rtype: None
        :raise RemoveError: If the symbol cannot be removed from the grammar.
        """
        if symbol not in self.alphabet:
            raise RemoveError(self.GRAMMAR, "alphabet", symbol=str(symbol))

        self.alphabet.remove(symbol)

    def add_non_terminal(self, symbol):
        """
        This method adds a new non-terminal to the grammar.

        :param symbol: The symbol to add to the grammar.
        :type symbol: str
        :return: None
        :rtype: None
        :raise AddError: If the symbol cannot be added to the grammar.
        """
        if symbol in self.non_terminals or symbol in self.alphabet:
            raise AddError(self.GRAMMAR, "states", symbol=str(symbol))

        self.non_terminals.add(symbol)

    def remove_non_terminal(self, symbol):
        """
        This method removes a non-terminal from the grammar.

        :param symbol: The symbol to remove from the grammar.
        :type symbol: str
        :return: None
        :rtype: None
        :raise RemoveError: If the symbol cannot be removed from the grammar.
        """
        if symbol not in self.non_terminals:
            raise RemoveError(self.GRAMMAR, "states", symbol=str(symbol))

        self.non_terminals.remove(symbol)

    def add_rule(self, left, right):
        """
        This method adds a new rule to the grammar.
        :param left: The left side of the rule.
        :type left: str
        :param right: The right side of the rule.
        :type right: str
        :return: None
        :rtype: None
        :raise AddError: If the left side of the rule cannot be added to the grammar.
        """
        if not left or not right:
            raise AddError(self.GRAMMAR, "rules", lhs=left, rhs=right)

class LBA(Automaton):

    GRAMMAR = "Context-Sensitive"
    TYPE = CHOMSKY_GRAMMARS[GRAMMAR] - 1