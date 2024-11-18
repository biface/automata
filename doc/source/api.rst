Package reference
=================

For greater convenience, the modules remain hidden inside the package. These modules are exposed for development
purposes only.

.. module:: fsm_tools
    :no-index:

Exceptions
----------

.. automodule:: fsm_tools.exception
    :private-members: StateMachineException, StateMachineTypeError, StateMachineValueError
.. autoexception:: FSMTransitionError
.. autoexception:: FSMTriggerError

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