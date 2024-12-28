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

from typing import List, Any

from .constants import CHOMSKY_GRAMMARS
from .exception import ReadError, AddError, RemoveError, ModifyError, RemoveComponentError


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

    def get_type(self) -> int:
        """
        Returns the type of the automaton (e.g., finite state automaton, Turing machine, etc.).

        :return: The type of the grammar (type 0, 1, 2, 3)
        :rtype: int
        """
        return self.automaton.TYPE

    def reset_alphabet(self):
        """
        Resets the alphabet (terminal symbols) of the grammar to an empty set.

        This method is useful when the alphabet needs to be redefined from scratch.
        """
        self.alphabet = set()

    def reset_states(self):
        """
        Resets the states (non-terminal symbols) of the grammar to an empty set.

        This method is useful when the set of states needs to be redefined from scratch.
        """
        self.states = set()

    def reset_rules(self):
        """
        Resets the list of production rules to an empty list.

        This method is useful when the set of rules needs to be redefined from scratch.
        """

        self.rules = []

    def reset(self):
        """
        Resets all components of the grammar: alphabet, states, and rules.

        This method provides a full reset of the grammar, clearing all components and allowing
        for a fresh definition of the grammar.
        """
        self.reset_alphabet()
        self.reset_states()
        self.reset_rules()


class Automaton:
    """
    Represents the base class for automata, providing a structure for automata that process
    formal grammars. This class serves as the foundation for specific types of automata, such as
    DFA, PDA, LBA, or TM, that can be used to recognize or generate strings based on the rules
    of a given grammar.

    Attributes:
        GRAMMAR (str): Reference to Chomsky grammar hierarchy (e.g., "Regular", "Context-Free").
        TYPE (int): Reference to Chomsky grammar hierarchy type, which corresponds to the automaton's type.
        name (str): The name of the automaton. This can be used to identify different types of automata.
        grammar (Grammar): An empty Grammar object initialized as part of the automaton. The grammar can
                           be populated later with terminals, non-terminals, and rules.
    """

    GRAMMAR: str = ""
    TYPE: int = 99

    def __init__(self, name: str = "", chomsky: str = None):
        """
        Initializes the Automaton with a given name and a given Grammar classification name.

        :param name: The name of the automaton, which can be used to identify the automaton.
        :type name: str
        :param chomsky: The Chomsky grammar classification type to be used, which defines the automaton's behavior.
        :type chomsky: str | None
        :raise KeyError: If the given Chomsky grammar type is not recognized.
        """
        self.name = name
        if chomsky is not None and chomsky in CHOMSKY_GRAMMARS.keys():
            self.GRAMMAR = chomsky
            self.TYPE = CHOMSKY_GRAMMARS[chomsky] - 1
        else:
            raise KeyError(f"Chomsky hierarchy: key '{chomsky}' not recognized.")
        self.grammar = Grammar(self)

    def get_terminals(self, ):
        """
        Returns the set of terminal symbols (alphabet) used in the grammar.

        :return: A set of terminal symbols.
        :rtype: set
        :raise ReadError: If no terminals have been defined in the grammar.
        """
        if len(self.grammar.alphabet) == 0:
            raise ReadError(self.GRAMMAR, 'alphabet')
        else:
            return self.grammar.alphabet

    def add_terminals(self, *terminals: any):
        """
        Adds terminal symbols to the grammar's alphabet.

        :param terminals: One or more terminal symbols to be added.
        :raise AddError: If a symbol is already in the alphabet or states.
        """
        for symbol in terminals:
            if symbol not in self.grammar.alphabet and symbol not in self.grammar.states:
                self.grammar.alphabet.add(symbol)
            else:
                raise AddError(self.GRAMMAR, "alphabet", symbol=symbol)

    def remove_terminals(self, *terminals: any):
        """
        Removes terminal symbols from the grammar's alphabet.

        :param terminals: One or more terminal symbols to be removed.
        :raise RemoveError: If a symbol is not found in the alphabet.
        """
        for symbol in terminals:
            if symbol in self.grammar.alphabet:
                self.grammar.alphabet.remove(symbol)
            else:
                raise RemoveError(self.GRAMMAR, "alphabet", symbol=symbol)

    def modify_terminal(self, existing_terminal: any, new_terminal: any):
        """
        Modifies an existing terminal symbol by removing it and adding a new one.

        :param existing_terminal: The terminal symbol to be replaced.
        :param new_terminal: The new terminal symbol to add.
        :raises AddError: If the new terminal is already present in the alphabet.
        :raises ModifyError: If the existing terminal cannot be modified due to errors.
        """
        try:
            self.remove_terminals(existing_terminal)
            self.add_terminals(new_terminal)
        except AddError as e:
            raise e
        except RemoveError:
            raise ModifyError(self.GRAMMAR, "alphabet", symbol=existing_terminal)

    def withdraw_terminal(self):
        """
        Clears all terminal symbols (alphabet) from the grammar.

        :raise ReadError: If the alphabet is empty when trying to withdraw terminals.
        """
        if len(self.grammar.alphabet) == 0:
            raise ReadError(self.GRAMMAR, 'alphabet')
        else:
            self.grammar.reset_alphabet()

    def get_states(self):
        """
        Returns the set of non-terminal symbols (states) used in the grammar.

        :return: A set of non-terminal symbols (states).
        :rtype: set
        :raise ReadError: If no states have been defined in the grammar.
        """
        if len(self.grammar.states) == 0:
            raise ReadError(self.GRAMMAR, 'states')
        else:
            return self.grammar.states

    def add_non_terminals(self, *non_terminals: any):
        """
        Adds non-terminal symbols to the grammar's set of states.

        :param non_terminals: One or more non-terminal symbols to be added.
        :raise AddError: If a symbol is already in the states.
        """
        for symbol in non_terminals:
            if symbol not in self.grammar.states:
                self.grammar.states.add(symbol)
            else:
                raise AddError(self.GRAMMAR, "states", symbol=symbol)

    def remove_non_terminals(self, *non_terminals: any):
        """
        Removes non-terminal symbols from the grammar's set of states.

        :param non_terminals: One or more non-terminal symbols to be removed.
        :raise RemoveError: If a symbol is not found in the states.
        """
        for symbol in non_terminals:
            if symbol in self.grammar.states:
                self.grammar.states.remove(symbol)
            else:
                raise RemoveError(self.GRAMMAR, "states", symbol=symbol)

    def modify_non_terminal(self, existing_non_terminal: any, new_non_terminal: any):
        """
        Modifies an existing non-terminal symbol by removing it and adding a new one.

        :param existing_non_terminal: The non-terminal symbol to be replaced.
        :param new_non_terminal: The new non-terminal symbol to add.
        :raises AddError: If the new non-terminal is already present in the states.
        :raises ModifyError: If the existing non-terminal cannot be modified due to errors.
        """
        try:
            self.remove_non_terminals(existing_non_terminal)
            self.add_non_terminals(new_non_terminal)
        except AddError as e:
            raise e
        except RemoveError:
            raise ModifyError(self.GRAMMAR, "states", symbol=existing_non_terminal)

    def withdraw_non_terminal(self):
        """
        Clears all non-terminal symbols (states) from the grammar.

        :raise ReadError: If the states are empty when trying to withdraw non-terminals.
        """
        if len(self.grammar.states) == 0:
            raise ReadError(self.GRAMMAR, 'states')
        else:
            self.grammar.reset_states()

    def get_rules(self):
        """
        Returns the list of production rules used in the grammar.

        :return: A list of production rules.
        :rtype: list
        :raise ReadError: If no rules have been defined in the grammar.
        """
        if len(self.grammar.rules) == 0:
            raise ReadError(self.GRAMMAR, 'rules')
        else:
            return self.grammar.rules

    def add_rules(self, *rules: any):
        """
        Adds production rules to the grammar.

        :param rules: One or more production rules to be added.
        """
        for rule in rules:
            if rule not in self.grammar.rules:
                self.grammar.rules.append(rule)

    def remove_rules(self, *rules: any):
        """
        Removes production rules from the grammar.

        :param rules: One or more production rules to be removed.
        :raise RemoveError: If a rule is not found in the grammar's list of rules.
        """
        for rule in rules:
            if rule not in self.grammar.rules:
                raise RemoveError(self.GRAMMAR, 'rules', symbol=rule)
            else:
                self.grammar.rules.remove(rule)

    def withdraw_rules(self):
        """
        Clears all production rules from the grammar.

        :raise RemoveComponentError: If the rules are empty when trying to withdraw rules.
        """
        if len(self.grammar.rules) == 0:
            raise RemoveComponentError(self.GRAMMAR, 'rules')
        else:
            self.grammar.reset_rules()

    def withdraw_grammar(self):
        """
        Clears all components of the grammar (alphabet, states, rules).

        This method provides a full reset of the grammar, clearing all its components.
        """
        self.grammar.reset()


class TuringMachine(Automaton):
    """
    Represents a Turing Machine (TM), a type of automaton capable of simulating any algorithm.
    It extends the base `Automaton` class to incorporate specific attributes and operations
    needed for Turing Machine computation. The machine operates on a tape and has the ability
    to read, write, and move the head along the tape based on predefined rules.

    This Turing Machine is specifically associated with the processing of **Type 0 languages**,
    which are also known as **recursively enumerable languages**. Type 0 languages represent the
    most general class of languages in the Chomsky hierarchy, which includes all languages that
    can be recognized by a Turing Machine. These languages are not necessarily decidable, but they
    can be enumerated by a machine that may not halt for all inputs.

    Attributes:
        tape (list): The tape (or tape array) that the Turing Machine operates on. Each cell in
                     the tape contains a symbol from the alphabet. The tape is considered
                     infinite in both directions, and its cells are initially filled with the blank symbol.
        head (int): The position of the read/write head on the tape. The head moves left or right
                    based on the machine's transition rules.
        register (str): The current state of the Turing Machine. This is used to determine the
                        next action based on the current state and the symbol under the head.
        blank (str): The blank symbol, representing an empty or uninitialized tape cell.
        moves (str): Defines movements allowed to the Turing Machine. Default moves allowed are forward (**F**) and
                     backward (**B**). Turing Machines may have more than 2 movements.
        state (dict): A dictionary that stores the accept and reject states of the Turing Machine.
                      The machine halts when it enters the accept or reject state.

    Methods:
        step(self):
            Executes one step of the Turing Machine based on the current state and the symbol under
            the head. The machine transitions to a new state, writes a symbol, and moves the head.
            The transition is determined by the current state and symbol, based on the rules defined
            in `self.grammar.rules`.

        get_rules(self):
            Returns the list of current rules or transition actions. These rules are associated with
            the grammar of the Turing Machine.

    Associations:
        - The `self.grammar.rules` attribute will contain the set of transition rules for the Turing Machine.
          Each rule is typically represented as a tuple or structured action that includes:
          - The current state (`state_from`)
          - The current symbol being read (`symbol`)
          - The next state to transition to (`state_to`)
          - The symbol to write on the tape (`write_symbol`)
          - The direction to move the head (`L` or `R` for left or right).

        - `self.grammar.alphabet`: The alphabet of the Turing Machine includes both the symbols that the
          machine can read from and write to the tape, as well as the blank symbol. Each symbol in the tape
          should belong to this alphabet.

        - `self.grammar.states`: The set of states includes the machine’s current state and any states involved
          in transitions. The accept and reject states are also included, and the machine halts when it reaches
          one of these states.

        - `self.grammar.rules`: A list of rules that define the machine's behavior. Each rule maps a pair of
          current state and symbol to a next state, symbol to write, and head movement direction.

    Additional Parameters:
        - The blank symbol (`blank`) is used to represent an empty tape cell. This is an important
          concept for Turing Machines, as it defines the boundary of the non-empty portion of the tape.
          The blank symbol is added to the alphabet and used throughout the computation.

        - `state`: The dictionary that holds the names of the accept and reject states. These are crucial for
          halting the machine when the computation is finished or when the input is rejected.

    Notes:
        - Turing Machines are associated with **Type 0 languages** (recursively enumerable languages) in the Chomsky
          hierarchy, which are the most general class of formal languages. Type 0 languages include all languages
          that can be recognized by a Turing Machine, regardless of whether they are decidable or not.

        - A Turing Machine can perform unbounded computations on an infinite tape, making it capable of recognizing
          languages that are undecidable but still recursively enumerable.

        - The transition rules (`self.grammar.rules`) are crucial to the functionality of the machine, as they
          define how the machine progresses through its states based on the current symbol on the tape.

        - The machine halts when it enters either the accept or reject state, signifying that the computation
          is complete or that the input is rejected.

    """

    def __init__(self, name: str, axes: int = 1, blank_symbol: str = "_", movement: dict = {"F": [1], "B": [-1]},
                 register: str = "", accept: str = "OK", reject: str = "nOK"):
        """
        Initializes the Turing Machine with a given name and the blank symbol (defaults to "_").
        Inherits from the base `Automaton` class and initializes the tape, head, index, and
        register. Also, the blank symbol is set, and accept/reject states are added to the machine.

        :param name: The name of the machine to be initialized.
        :type name: str
        :param axes: The axes of the machine to be initialized.
        :type axes: int
        :param blank_symbol: The blank symbol, representing an empty or uninitialized tape cell.
        :type blank_symbol: str | "_"
        :param movement: dictionary of movement
        :type movement: dict
        :param register: The current state of the Turing Machine. This is used to determine the next action based on the current state and the symbol under the head.
        :type register: str | ""
        :param accept: The accept state to be initialized.
        :type accept: str | "OK"
        :param reject: The reject state to be initialized.
        :type reject: str | "nOK"
        """
        super().__init__(name, "Recursively Enumerable")
        self.axes = axes
        self.tape = []
        self.head = [0] * axes
        self.register = register
        self.blank = blank_symbol
        self.moves = movement
        self.add_terminals(blank_symbol)
        self.add_non_terminals(register)
        self.state = dict([('accept', accept), ('reject', reject)])
        self.add_non_terminals(accept)
        self.add_non_terminals(reject)

    def _initialize_tape(self):
        """
        Initializes the tape as a nested list
        """

        def create_nested_list(depth):
            if depth == 0:
                return self.blank  # Une cellule du ruban
            return [create_nested_list(depth - 1)]

        return create_nested_list(self.axes)

    def _extend_tape(self, location: list) -> None:
        """
        Extends the tape dynamically to accommodate the current head position.

        :param location: The current head position
        :type location: list
        :return: None
        :rtype: None
        """

    def set_tape(self, content: List[Any], location:List[int] = None) -> None:
        """
        Initializes the tape with a list of symbols and places the head at the starting index. The tape_content list
        must contain only symbols from the machine's alphabet.

        :param content: The list of symbols to place in the tape.
        :type content: list
        :param location: The current head position
        :type location: list
        :return: None
        :rtype: None
        :raise ReadError: If any symbol in the tape_content is not part of the alphabet.
        """
        for content in self.tape:
            for symbol in content:
                if symbol not in self.get_terminals():
                    ReadError(self.GRAMMAR, "alphabet", symbol=symbol)
        self.tape = content

        if location is None:
            location = [0] * self.axes

        self.head = location
        self._extend_tape(self.head)

    def set_register(self, register: str) -> None:
        """
        Initializes the register with a list of symbols and places the head at the starting index.

        :param register: The list of symbols to place in the tape.
        :type register: str
        :return: None
        :rtype: None
        """
        self.register = register

    def set_moves(self, **moves) -> None:
        """
        Initializes the moves with a list of symbols and places the head at the starting index.

        :param moves: The list of symbols to place in the tape.
        :type moves: list of str
        :return: None
        :rtype: None
        """
        self.moves = moves

    def read(self) -> Any:
        """Read the symbol at the current position of the head."""
        self._extend_tape(self.head)
        current_cell = self.tape
        for index in self.head:
            if index < 0 or index >= len(current_cell):
                raise IndexError(f"Head position {self.head} is out of bounds.")
            current_cell = current_cell[index]
        return current_cell

    def write(self, symbol: any) -> None:
        """
        Writes a symbol at the current head position on the multidimensional tape.
        If the symbol is not already part of the alphabet, it is added automatically.

        :param symbol: The symbol to write at the current head position
        :type symbol: any
        :return: None
        :rtype: None
        """
        # Check if the symbol is part of the alphabet, add it if not
        if symbol not in self.grammar.alphabet:
            self.add_terminals(symbol)

        # Ensure the tape is extended to accommodate the current head position
        self._extend_tape(self.head)

        # Navigate to the correct position on the tape and write the symbol
        current_cell = self.tape
        for i, index in enumerate(self.head):
            if i == len(self.head) - 1:
                current_cell[index] = symbol
            else:
                current_cell = current_cell[index]

    def move(self, direction: str) -> None:
        """
        Moves the head of the Turing Machine in the specified direction.

        :param direction: The direction to move the head of the Turing Machine
        :type direction: str
        :return: None
        :rtype: None
        """
        if direction not in self.moves:
            raise ValueError(f"Invalid direction '{direction}'. Must be one of {list(self.moves.keys())}.")

        # Get the movement increments for the given direction
        axis = 0
        if self.axes > 1 or isinstance(self.moves[direction], list):
            for dx in self.moves[direction]:
                self.head[axis] = self.head[axis] + dx
                axis += 1
        else:
            self.head[axis] = self.head[axis] + self.moves[direction]

    def add_transition(self, state_from: str, symbol: any, state_to: str, write_symbol: any, move_direction):
        """
        Adds a transition rule to the Turing Machine's transition table. This rule defines
        what the Turing Machine should do when it encounters a specific symbol in a given state.

        A transition for a Turing Machine includes the following components:

        - The current state (`state_from`): The state the machine is in before performing the action.
        - The current symbol (`symbol`): The symbol that is under the machine's read/write head (can be of any type).
        - The next state (`state_to`): The state the machine should transition to.
        - The symbol to write (`write_symbol`): The symbol to be written on the tape (can be of any type).
        - The direction to move (`move_direction`): The direction in which the head should move after writing the symbol ('L' for left, 'R' for right).

        These components align with the formal components of a Type-0 grammar (recursively enumerable grammar):

        - The **states** of the machine correspond to the non-terminals in the grammar.
        - The **symbols** under the head correspond to the terminals in the grammar.
        - The **transition rules** themselves can be considered as production rules in the grammar that specify how non-terminals (states) interact with terminals (symbols).

        This method adds the transition to the Turing Machine's internal transition table, which is stored in `self.grammar.rules`.
        The rules can be seen as a form of production that modifies the state and the tape contents.

        :param state_from: The current state of the machine.
        :type state_from: str
        :param symbol: The symbol under the head of the machine.
        :type symbol: any
        :param state_to: The current state of the machine.
        :type state_to: str
        :param write_symbol: The symbol to write on the tape.
        :type write_symbol: any
        :param move_direction: The direction to move the head, should be one of the valid directions in `self.move`.
        :type move_direction: str
        :return: None
        :rtype: None
        :raises ReadError: If the symbol is not in the alphabet of the Turing Machine.
        :raises ValueError: If the symbol is not in the alphabet of the Turing Machine.
        """
        # First, ensure the symbol is in the alphabet of the machine.
        if symbol not in self.get_terminals():
            raise ReadError(self.GRAMMAR, 'alphabet', symbol=symbol)

        # Ensure that the direction is valid (either 'L' or 'R').
        if move_direction not in self.moves:
            raise ValueError(f"Invalid move direction '{move_direction}'. Must be {self.moves}.")

        # Add the transition rule to the list of rules (grammar rules).
        transition_rule = (state_from, symbol, state_to, write_symbol, move_direction)
        self.add_rules(transition_rule)  # Adding the rule to the machine's grammar rules.

    def step(self):
        """Execute one step of the Turing Machine based on current state and symbol."""
        current_symbol = (self.read())
        # Iterate over the transition rules in self.grammar.rules
        for rule in self.grammar.rules:
            state_from, symbol, state_to, write_symbol, move_direction = rule
            if self.register == state_from and current_symbol == symbol:
                # Perform the transition: write, move, and change state
                self.write(write_symbol)
                self.move(move_direction)
                self.register = state_to
                self.add_non_terminals(state_to)  # Add the new state to the set of states
                break  # Exit after finding and executing a valid rule
        else:
            raise Exception(f"No valid transition for state '{self.register}' and symbol '{current_symbol}'.")
