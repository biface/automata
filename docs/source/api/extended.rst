Extended Automata
=================

This page documents the pedagogical extensions defined in ``fsm_tools.extended``.
These classes extend the formal Chomsky hierarchy with n-dimensional tape support,
illustrating how a richer computational model can be built within the same grammar
classification (see :doc:`/theory/chomsky/automata`).

.. note::

   The n-dimensional tape extension does **not** change the class of languages
   recognised. ``ExtendedTuringMachine`` still recognises exactly the same Type 0
   languages as :class:`~fsm_tools.TuringMachine`. This is a direct illustration
   of the Church-Turing thesis.

ExtendedTuringMachine
---------------------

.. autoclass:: fsm_tools.ExtendedTuringMachine
   :members:
   :show-inheritance:

ExtendedLBA
-----------

.. autoclass:: fsm_tools.ExtendedLBA
   :members:
   :show-inheritance:
