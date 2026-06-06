The Chomsky Hierarchy
=====================

The Chomsky hierarchy classifies formal languages — and the automata that recognise
them — into four nested families. Each level is a strict restriction of the one above
it: a more constrained grammar, a less powerful machine, a smaller class of languages.

.. list-table::
   :header-rows: 1
   :widths: 10 30 30 30

   * - Type
     - Grammar
     - Automaton
     - Language family
   * - 0
     - Unrestricted
     - Turing Machine
     - Recursively enumerable
   * - 1
     - Context-sensitive
     - Linear Bounded Automaton
     - Context-sensitive
   * - 2
     - Context-free
     - Pushdown Automaton
     - Context-free
   * - 3
     - Regular
     - Finite State Automaton
     - Regular

This section covers the theoretical foundations of each level and its implementation
in **fsm-tools**.

.. toctree::
   :maxdepth: 2

   alphabet
   kleene
   chomsky
   automata
