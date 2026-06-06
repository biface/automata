Introduction to Formal Language Theory
======================================

Formal language theory and automata provide the mathematical foundation for understanding
how computational systems operate and how structured languages are defined and processed.

Automata are abstract models of machines that perform operations on an input by passing
through a series of states or configurations. At each state, a transition function
determines the next state based on all or part of the current configuration. When the
computation reaches an accepting configuration, the input is accepted.

**fsm-tools** implements these models rigorously, following the formal structure of
Chomsky's hierarchy. Each automaton in the library corresponds directly to a class of
formal languages.

Key concepts
------------

The following chapters introduce the theoretical foundations required to understand
and use the library:

- **Alphabet, Grammar and Language** — the basic building blocks of any formal language.
- **The Kleene Star** — the closure operator that generates infinite languages from
  finite alphabets.
- **The Chomsky Hierarchy** — the four-level classification of grammars and their
  corresponding automata.

These concepts are presented in a logical progression. Each chapter cross-references
the corresponding implementation class in the :doc:`/api/advanced`.

.. seealso::

   :doc:`grammar` — the ``Grammar`` object as implemented in **fsm-tools**.

   :doc:`/guide/quickstart` — runnable examples for each automaton type.
