Overview
========

**Finite State Machine tools** is a toolbox designed to manage finite-state automata. This toolbox has been extended to
handle the addition of data to the contexts used in the templates of the django framework.

**Automata** are abstract models of machines that perform operations on an input by passing through a series of states or
configurations. At each state, a transition function determines the next state or configuration based on all or part of
the current state or configuration. When the calculation reaches an acceptance configuration, it accepts this input.
The most general and powerful automaton is the **Turing machine**.

These automata are very useful for modeling processes and workflows. They are often the basis of many application flows,
without being properly formalized and managed.

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
