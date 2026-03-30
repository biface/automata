Overview
========

**Finite State Machine tools** is a comprehensive toolbox originally designed to manage finite-state automata (FSM).
Over time, this toolbox has been extended to support additional types of automata, reflecting the broader scope of
Chomsky's grammar and language hierarchy. The package name remains the same, but its capabilities have grown significantly.

**Automata** are abstract models of machines that perform operations on an input by passing through a series of states
or configurations. At each state, a transition function determines the next state or configuration based on all or part
of the current state or configuration. When the calculation reaches an acceptance configuration, it accepts the input.
The most general and powerful automaton is the **Turing machine**, capable of simulating any computational process.

This package supports the following types of automata, aligned with their respective positions in Chomsky's hierarchy of languages:

- **Finite-state automata (FSA):** Correspond to regular languages (Type 3). These automata are simple and efficient for
  modeling workflows, processes, and event-driven systems.
- **Pushdown automata (PDA):** Linked to context-free languages (Type 2), enabling the modeling of nested structures
  like those found in programming languages.
- **Linearly bounded automata (LBA):** Associated with context-sensitive languages (Type 1), suitable for systems with
  constraints on memory usage.
- **Turing machines:** Represent recursively enumerable languages (Type 0) and serve as the foundation for understanding
  general computation.

These automata are invaluable for modeling processes and workflows. They form the backbone of many applications, often
invisibly driving processes without being explicitly formalized or managed.

**Finite State Machine tools** also includes enhancements for integrating automata with modern frameworks. Notably, it
provides mechanisms to add data to the contexts used in templates for the Django framework, allowing developers to
seamlessly utilize automata in web development workflows.

.. toctree::
    install
    theory
    api
    :numbered:
    :maxdepth: 2
    :caption: Content
    :name: maintoc

Indices and references
======================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
