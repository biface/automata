User Guide
==========

This page covers the patterns and conventions needed to use **fsm-tools** correctly.

API stability
-------------

**fsm-tools** follows `Semantic Versioning <https://semver.org>`_. The current version
is **Pre-Alpha** (v0.1.0). The public API may change between minor versions until
v0.6.0 (Beta), at which point the API is frozen and no breaking changes are permitted
without a major version bump.

All breaking changes are documented in the :doc:`install` version history and in the
`CHANGELOG <https://github.com/biface/automata/blob/master/CHANGELOG.md>`_.

The ``chomsky`` parameter
--------------------------

Every automaton in the Chomsky hierarchy requires the ``chomsky`` keyword parameter.
It is mandatory — omitting it raises ``TypeError``:

.. code-block:: python

   from fsm_tools import Automaton

   a = Automaton(name="test")                        # TypeError
   a = Automaton(name="test", chomsky="Regular")     # OK

The valid values are ``"Regular"``, ``"Context-Free"``, ``"Context-Sensitive"``,
and ``"Recursively Enumerable"``. Concrete subclasses set this automatically —
you never pass it when using :class:`~fsm_tools.TuringMachine`,
:class:`~fsm_tools.LinearBoundedAutomaton`, or :class:`~fsm_tools.PushdownAutomaton`.

Exception handling
------------------

All exceptions in **fsm-tools** inherit from :class:`~fsm_tools.AutomatonException`.
Each exception carries:

- A unique numeric **error code** computed from the grammar level, component, and action.
- A human-readable **message** in English (en-US).

.. code-block:: python

   from fsm_tools import PushdownAutomaton
   from fsm_tools.exception import AddError, ReadError, ValidationError

   pda = PushdownAutomaton(name="p", stack_alphabet={"A"})
   pda.add_terminals("a")
   pda.set_register("q0")

   try:
       pda.add_transition("q0", "a", "X", "q0", [])  # "X" not in stack_alphabet
   except AddError as e:
       print(e)        # human-readable message
       print(e.value)  # numeric error code

The exception hierarchy maps directly onto the available actions:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Exception
     - Action
     - Typical cause
   * - :class:`~fsm_tools.ReadError`
     - ``read``
     - Empty alphabet, empty states
   * - :class:`~fsm_tools.AddError`
     - ``add``
     - Duplicate symbol, duplicate transition
   * - :class:`~fsm_tools.RemoveError`
     - ``remove``
     - Symbol not found
   * - :class:`~fsm_tools.ModifyError`
     - ``modify``
     - Target not found
   * - :class:`~fsm_tools.ValidationError`
     - ``validate``
     - Automaton not configured
   * - :class:`~fsm_tools.SearchError`
     - ``search``
     - Element not found
   * - :class:`~fsm_tools.RemoveComponentError`
     - ``withdraw``
     - Component empty (e.g. empty stack pop)

Building an automaton step by step
------------------------------------

The typical construction sequence for any automaton is:

1. Instantiate the class.
2. Add terminal symbols (input alphabet).
3. Set the initial state via ``set_register()``.
4. Add any additional states via ``add_non_terminals()``.
5. Add transition rules via ``add_transition()``.
6. Load input and run (``set_tape()`` + ``step()`` for TM/LBA,
   ``validate()`` for PDA).

.. code-block:: python

   from fsm_tools import PushdownAutomaton

   pda = PushdownAutomaton(name="example", stack_alphabet={"A"})
   pda.add_terminals("a", "b")          # step 2
   pda.set_register("q0")               # step 3
   pda.add_non_terminals("q1")          # step 4
   pda.add_transition(...)              # step 5
   pda.validate(["a", "b"])             # step 6

Known limitations in v0.1.0
-----------------------------

- **Epsilon-transitions** in :class:`~fsm_tools.PushdownAutomaton` are not yet
  implemented. Passing ``input_symbol=None`` raises ``NotImplementedError``.
  Planned for v0.3.0.

- **FiniteStateAutomaton** is not yet implemented. Planned for v0.2.0.

- **Non-determinism** is not supported — all automata are deterministic.
  The first matching transition rule is applied.

- **Error messages** for some stack operations use approximate codes pending
  the error management audit planned for v0.3.0.

.. seealso::

   :doc:`quickstart` — working examples for each automaton type.

   :doc:`/api/exceptions` — full exception reference.
