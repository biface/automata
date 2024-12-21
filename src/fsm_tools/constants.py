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

# Components within automata
COMPONENTS = {
        'alphabet': 1,
        'states': 3,
        'transitions': 2,
        'stack': 5,
        'grammar': 4,
        'validation': 6
    }

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