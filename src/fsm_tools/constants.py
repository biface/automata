"""
This file contains constants that will be used to manage the components, actions and grammars of the Chomsky hierarchy
and automata.
"""

# Chomsky hierarchy levels (Grammar types)
CHOMSKY_GRAMMARS = {
    "Regular": 4,
    "Context-Free": 3,
    "Context-Sensitive": 2,
    "Recursively Enumerable": 1,
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
# Components within automata — 8 primary axes, each needing its own explanatory
# treatment in the message catalogs, plus aliases that are pure usage-vocabulary
# translations of a primary axis (same integer, no distinct message content of
# their own). See DD-004/DD-009 and issue #79 for the full rationale.
COMPONENTS = {
    # Primary axes
    "alphabet": 1,  # Sigma, terminal symbols
    "transitions": 2,  # delta realised as machine transitions (FSA, TM; also the
    # raw transition CRUD shared by LBA/PDA alongside "grammar")
    "non_terminals": 3,  # N, the formal non-terminal set
    "grammar": 4,  # P realised as production rules (PDA, LBA — distinct
    # message content from "transitions", e.g. malformed rule)
    "stack": 5,  # LIFO memory of a pushdown automaton
    "validation": 6,  # automaton-level and word-level validation outcomes
    "tape": 7,  # TM/LBA tape mechanics (read/write/move, boundary checks)
    "register": 8,  # current-state pointer, distinct from non_terminals (the set)
    # Aliases — pure usage-vocabulary translation of a primary axis above.
    # No distinct message content: resolve to the same integer as their axis.
    "states": 3,  # non_terminals, in automata-usage vocabulary
    "blank": 1,  # alphabet, the distinguished blank terminal
    "head": 7,  # tape, head-position manifestation
    "moves": 7,  # tape, movement manifestation
}
"""
COMPONENTS is a dictionary that assigns a unique integer value to each key
representing a fundamental component in computational models and formal grammar processing.

There are 8 primary axes (each with its own message content, in both the "automata" and
"errors" catalogs) and 4 aliases (pure usage-vocabulary translations that resolve to the
same integer as their primary axis, carrying no distinct message content of their own):
    - "states" -> "non_terminals" (N is the formal name; every message says "state")
    - "blank" -> "alphabet" (the blank symbol is a distinguished terminal)
    - "head" -> "tape", "moves" -> "tape" (both are manifestations of tape mechanics)

These integer values provide a straightforward way to reference or prioritize components
in computational workflows, and to compute a unique error code (see utils/common.py).
"""

# Per-subclass resolution of the "rules" concept (DD-009): which primary COMPONENTS
# axis a subclass's get_rules()/remove_rules()/withdraw_rules() should raise with,
# keyed by the automaton's own GRAMMAR classification (never a new instance attribute).
RULES_COMPONENT_BY_GRAMMAR = {
    "Regular": "transitions",
    "Recursively Enumerable": "transitions",
    "Context-Free": "grammar",
    "Context-Sensitive": "grammar",
}
"""
RULES_COMPONENT_BY_GRAMMAR resolves which COMPONENTS axis to use for the generic
get_rules()/remove_rules()/withdraw_rules() methods defined once on Automaton, since
the correct axis depends on the calling instance's Chomsky classification (DD-009):
FiniteStateAutomaton and TuringMachine expose delta as "transitions"; PushdownAutomaton
and LinearBoundedAutomaton expose P as "grammar" (context-free/context-sensitive
production rules). Looked up from self.GRAMMAR at call time — no separate state to keep
in sync with the class hierarchy.
"""

# Possible actions on components
ACTIONS = {
    "read": 1,
    "add": 2,
    "remove": 3,
    "modify": 4,
    "validate": 5,
    "search": 6,
    "withdraw": 19,
    "write": 7,
    "move": 8,
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
