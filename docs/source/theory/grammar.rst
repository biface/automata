Grammar as a Data Structure
===========================

In **fsm-tools**, a grammar is not merely a type annotation or a string constant —
it is a full Python object, instantiated and owned by each :class:`~fsm_tools.Automaton`
instance. This design follows directly from the formal definition of a grammar in
language theory (see :ref:`grammar-formal-definition`).

.. _grammar-formal-definition:

Formal definition
-----------------

A grammar :math:`G` is a quadruple :math:`G = (N,\ \Sigma,\ P,\ S)` where:

- :math:`N` is a finite set of **non-terminal** symbols (states).
- :math:`\Sigma` is a finite set of **terminal** symbols (the alphabet), disjoint from :math:`N`.
- :math:`P` is a finite set of **production rules**.
- :math:`S \in N` is the **start symbol**.

The nature of :math:`P` — what forms a valid production rule — is what distinguishes
the four levels of the Chomsky hierarchy from one another.

Implementation
--------------

The :class:`~fsm_tools.Grammar` class maps directly onto this quadruple:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Formal component
     - Attribute
     - Description
   * - :math:`N`
     - ``grammar.states``
     - Set of non-terminal symbols (automaton states).
   * - :math:`\Sigma`
     - ``grammar.alphabet``
     - Set of terminal symbols (input alphabet).
   * - :math:`P`
     - ``grammar.rules``
     - List of production rules (format depends on automaton type).
   * - :math:`S`
     - ``grammar.start``
     - Start symbol — the initial state of the automaton.

Design principle
----------------

The :class:`~fsm_tools.Grammar` object is owned by its automaton. All mutations
go through the :class:`~fsm_tools.Automaton` API methods (``add_terminals``,
``add_non_terminals``, ``add_rules``, …). Direct access to ``automaton.grammar.alphabet``
is technically possible but discouraged — the automaton API is the stable contract.

.. code-block:: python

   from fsm_tools import TuringMachine

   tm = TuringMachine(name="example", chomsky="Recursively Enumerable")
   tm.add_terminals("a", "b")       # modifies grammar.alphabet
   tm.add_non_terminals("q0", "q1") # modifies grammar.states

   print(tm.grammar.alphabet)  # {'a', 'b', '_'}
   print(tm.grammar.states)    # {'q0', 'q1', 'OK', 'nOK'}

.. note::

   The blank symbol (``_`` by default for :class:`~fsm_tools.TuringMachine`) is
   added to the alphabet automatically at initialisation.

.. seealso::

   :class:`~fsm_tools.Grammar` — full API reference.

   :doc:`chomsky/chomsky` — how production rules vary across the Chomsky hierarchy.
