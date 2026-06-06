Exceptions
==========

All exceptions in **fsm-tools** inherit from :class:`~fsm_tools.AutomatonException`.
Each exception carries a unique numeric error code computed from three axes:

The error code is computed as follows::

    code = 1000 × CHOMSKY_GRAMMARS[grammar]
         +  100 × COMPONENTS[component]
         +    1 × ACTIONS[action]

Given any code, the grammar level, component, and action can be recovered
unambiguously. All messages are in English (en-US).

.. module:: fsm_tools.exception
   :no-index:

Base classes
------------

.. autoclass:: fsm_tools.AutomatonException
   :members:
   :show-inheritance:

.. autoclass:: fsm_tools.AutomatonError
   :members:
   :show-inheritance:

Typed exceptions
----------------

.. autoclass:: fsm_tools.ReadError
   :show-inheritance:

.. autoclass:: fsm_tools.AddError
   :show-inheritance:

.. autoclass:: fsm_tools.RemoveError
   :show-inheritance:

.. autoclass:: fsm_tools.ModifyError
   :show-inheritance:

.. autoclass:: fsm_tools.ValidationError
   :show-inheritance:

.. autoclass:: fsm_tools.SearchError
   :show-inheritance:

.. autoclass:: fsm_tools.RemoveComponentError
   :show-inheritance:

Constants
---------

The following constants define the valid values for grammar levels, components,
and actions. They are used internally by the exception system.

.. automodule:: fsm_tools.constants
   :members:
   :no-index:
