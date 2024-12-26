"""
This file contains constants that will be used to manage the components, actions and grammars of the Chomsky hierarchy
and automata.
"""

# Chomsky hierarchy levels (Grammar types)
CHOMSKY_GRAMMARS = {
        'Regular': 4,
        'Context-Free': 3,
        'Context-Sensitive': 2,
        'Recursively Enumerable': 1
    }
"""
CHOMSKY_GRAMMAR is a dictionary that maps the different types of grammars 
in the Chomsky hierarchy to their corresponding integer values. These integer 
values are primarily used for message handling, error reporting, and processing 
purposes.

Each grammar type in the hierarchy is assigned a unique integer value based on 
its rank in the hierarchy. The values are incremented by 1 from their theoretical 
positions (e.g., Type-0 → 1, Type-1 → 2, etc.) to ensure the values are suitable 
for computation and indexing in various operations.

The mapping is as follows:
    - "Type-0" (Recursively Enumerable or Unrestricted Grammar): Value 1
    - "Type-1" (Context-Sensitive Grammar): Value 2
    - "Type-2" (Context-Free Grammar): Value 3
    - "Type-3" (Regular Grammar): Value 4

This structure allows the grammar types to be easily referenced and utilized in 
applications where a numeric representation is required.
"""
# Components within automata
COMPONENTS = {
        'alphabet': 1,
        'states': 3,
        'transitions': 2,
        'stack': 5,
        'grammar': 4,
        'validation': 6
    }
"""
COMPONENTS is a dictionary that assigns a unique integer value to each key 
representing a fundamental component in computational models and formal grammar processing. 

The integer values serve as identifiers, used for ordering, processing, or error handling 
in various operations. The values are assigned in a manner that reflects their relative 
importance or usage frequency in certain contexts.

The mapping is as follows:
    - "alphabet": Value 1 - Represents the set of terminal symbols in a grammar.
    - "states": Value 3 - Represents the set of non-terminal symbols or states in an automaton.
    - "transitions": Value 2 - Represents the rules or transitions that govern state changes.
    - "stack": Value 5 - Represents the stack used in pushdown automata.
    - "grammar": Value 4 - Represents the formal grammar associated with the automaton or model.
    - "validation": Value 6 - Represents the validation component for string recognition or processing.

These integer values provide a straightforward way to reference or prioritize components 
in computational workflows.
"""

# Possible actions on components
ACTIONS = {
        'read': 1,
        'add': 2,
        'remove': 3,
        'modify': 4,
        'validate': 5,
        'search': 6,
        'withdraw': 19
    }
"""
ACTIONS is a dictionary that maps common operations or actions to unique integer values, 
providing a standardized way to reference and process these actions in computational workflows.

The integer values are used as identifiers for ordering, prioritization, or error handling 
during the execution of various tasks. These values are designed to be consistent and 
easily computable.

The mapping is as follows:
    - "read": Value 1 - Represents the action of reading or retrieving data.
    - "add": Value 2 - Represents the action of adding new data or elements.
    - "remove": Value 3 - Represents the action of deleting or removing elements.
    - "modify": Value 4 - Represents the action of changing or updating existing data.
    - "validate": Value 5 - Represents the action of checking correctness or conformity.
    - "search": Value 6 - Represents the action of locating specific elements or data.
    - "withdraw": Value 19 - Represents the action of retracting or taking back elements.

These integer values ensure consistency in referencing actions across different modules 
or systems, enabling streamlined processing and error management.
"""