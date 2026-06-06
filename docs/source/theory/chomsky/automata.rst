Automata in fsm-tools
=====================

**fsm-tools** implements the Chomsky hierarchy as a strict Python inheritance chain.
Each class is a formal restriction of the one above it — it inherits the full structure
of its parent and constrains it further, removing degrees of freedom rather than adding them.

.. code-block:: text

   Automaton                              (abstract base)
   └── TuringMachine                      (Type 0 — recursively enumerable)
       └── LinearBoundedAutomaton         (Type 1 — context-sensitive)
           └── PushdownAutomaton          (Type 2 — context-free)
               └── FiniteStateAutomaton   (Type 3 — regular, planned v0.2.0)

This structure means that ``isinstance(pda, TuringMachine)`` is ``True`` — every
pushdown automaton is also a (constrained) Turing machine in the type system.

TuringMachine — Type 0
-----------------------

A Turing Machine operates on an infinite one-dimensional tape. Its transition function
maps a ``(state, symbol)`` pair to a ``(next_state, write_symbol, direction)`` triple.
It is the most general computational model — equivalent to any algorithm.

**Key properties:**

- Infinite bidirectional tape, extended dynamically with blank symbols.
- Read/write head moves left or right.
- Accepts when reaching the accepting state.

.. seealso:: :class:`~fsm_tools.TuringMachine`

LinearBoundedAutomaton — Type 1
--------------------------------

A Linear Bounded Automaton is a Turing Machine whose tape is bounded to a length
proportional to the input. It recognises exactly the context-sensitive languages.

**Restriction over TuringMachine:**

- Tape size bounded: ``limits`` enforced per dimension.
- Head raises ``IndexError`` if it reaches a tape boundary.

.. seealso:: :class:`~fsm_tools.LinearBoundedAutomaton`

PushdownAutomaton — Type 2
---------------------------

A Pushdown Automaton replaces the tape with a LIFO stack. Its transition function
maps a ``(state, input_symbol, stack_top)`` triple to a ``(next_state, stack_ops)``
pair, where ``stack_ops`` is the list of symbols pushed after popping the stack top.

**Restriction over LinearBoundedAutomaton:**

- No tape: memory is a stack (last-in, first-out).
- Input is read sequentially — no random access, no backtracking.
- Acceptance by empty stack (bottom marker convention).

**Transition 5-tuple:**

.. code-block:: python

   (state_from, input_symbol, stack_top, state_to, stack_ops)

Where ``stack_ops`` is a list of symbols pushed after popping ``stack_top``:

- ``[]`` — pure pop (no push).
- ``["A"]`` — replace top with ``A``.
- ``["A", "B"]`` — pop, then push ``B``, then ``A`` (``A`` ends on top).

.. note::

   Epsilon-transitions (``input_symbol=None``) are reserved and will be implemented
   in v0.3.0. Passing ``None`` raises ``NotImplementedError`` in v0.1.0.

.. seealso:: :class:`~fsm_tools.PushdownAutomaton`

FiniteStateAutomaton — Type 3
------------------------------

.. note::

   ``FiniteStateAutomaton`` is planned for **v0.2.0** and is not yet implemented.

A Finite State Automaton is a Pushdown Automaton with no stack: transitions depend
only on the current state and the current input symbol. It recognises exactly the
regular languages.

**Restriction over PushdownAutomaton:**

- No stack: transition function is ``(state, symbol) → state``.
- Accepts when reaching a designated accepting state after consuming all input.
