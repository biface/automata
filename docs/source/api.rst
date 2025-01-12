Package reference
=================

For greater convenience, the modules remain hidden inside the package. These modules are exposed for development
purposes only.

.. module:: fsm_tools
    :no-index:

Constants
---------

.. automodule:: fsm_tools.constants
.. autodata:: CHOMSKY_GRAMMARS
.. autodata:: COMPONENTS
.. autodata:: ACTIONS

Exceptions
----------

.. automodule:: fsm_tools.exception
.. autoexception:: AutomatonException
.. autoexception:: ReadError
.. autoexception:: AddError
.. autoexception:: RemoveError
.. autoexception:: ModifyError
.. autoexception:: ValidationError
.. autoexception:: SearchError
.. autoexception:: RemoveComponentError

Lightweight finite state machine
--------------------------------

.. automodule:: fsm_tools.lightweight
.. autoclass:: FSM

    .. autoattribute:: initial
    .. autoattribute:: current
    .. autoattribute:: transitions
    .. automethod:: add_transition
    .. automethod:: get_state
    .. automethod:: reset
    .. automethod:: trigger

.. autoclass:: ExtFSM

    .. automethod:: reset
    .. automethod:: get_previous
    .. automethod:: trigger

Django framework extensions
---------------------------

.. automodule:: fsm_tools.django
.. autoclass:: ContextFSM

    .. automethod:: as_dict
    .. automethod:: add_to_context

Advanced Automata
-----------------

.. automodule:: fsm_tools.advanced
.. autoclass:: Grammar

    .. automethod:: get_type
    .. automethod:: reset_alphabet
    .. automethod:: reset_states
    .. automethod:: reset_rules
    .. automethod:: reset

.. autoclass:: Automaton

    .. automethod:: get_terminals
    .. automethod:: add_terminals
    .. automethod:: remove_terminals
    .. automethod:: modify_terminal
    .. automethod:: withdraw_terminal
    .. automethod:: get_states
    .. automethod:: add_non_terminals
    .. automethod:: remove_non_terminals
    .. automethod:: modify_non_terminal
    .. automethod:: withdraw_non_terminal
    .. automethod:: get_rules
    .. automethod:: add_rules
    .. automethod:: remove_rules
    .. automethod:: withdraw_rules
    .. automethod:: withdraw_grammar

.. autoclass:: TuringMachine

    .. automethod:: set_tape
    .. automethod:: set_register
    .. automethod:: set_moves
    .. automethod:: read
    .. automethod:: write
    .. automethod:: move
    .. automethod:: add_transition

.. autoclass:: LinearBoundedAutomaton