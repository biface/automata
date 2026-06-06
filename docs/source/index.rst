fsm-tools
=========

A formal Python library for modelling automata in the Chomsky hierarchy.

**fsm-tools** provides a rigorous, educational implementation of the four automaton
families defined by Chomsky's grammar and language hierarchy. Each class is a formal
restriction of the one above it — inheriting its structure and constraining it further.

.. list-table::
   :header-rows: 1
   :widths: 10 30 35 25

   * - Type
     - Automaton
     - Language family
     - Status
   * - 0
     - :class:`~fsm_tools.TuringMachine`
     - Recursively enumerable
     - ✅ v0.0.4
   * - 1
     - :class:`~fsm_tools.LinearBoundedAutomaton`
     - Context-sensitive
     - ✅ v0.0.4
   * - 2
     - :class:`~fsm_tools.PushdownAutomaton`
     - Context-free
     - ✅ v0.1.0
   * - 3
     - ``FiniteStateAutomaton``
     - Regular
     - 🔄 planned v0.2.0

.. toctree::
   :maxdepth: 2
   :caption: Theory & Data Structures
   :numbered:

   theory/index

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :numbered:

   guide/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

Indices and references
----------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
