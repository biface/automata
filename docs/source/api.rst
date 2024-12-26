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
.. autoclass:: Automaton