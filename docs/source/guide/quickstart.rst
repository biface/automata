Quick Start
===========

This page shows minimal working examples for each implemented automaton type.
All examples assume **fsm-tools** is installed (see :doc:`install`).

Turing Machine — Type 0
------------------------

A simple Turing Machine that replaces every ``a`` with ``b`` on a 1D tape:

.. code-block:: python

   from fsm_tools import TuringMachine

   tm = TuringMachine(
       name="ReplaceA",
       chomsky="Recursively Enumerable",
       blank_symbol="_",
   )

   # Input alphabet
   tm.add_terminals("a", "b")

   # States
   tm.set_register("q0")
   tm.add_non_terminals("q1")

   # Tape movements
   tm.set_moves(R=[1], L=[-1])

   # Transitions: (state_from, read_symbol, state_to, write_symbol, direction)
   tm.add_transition("q0", "a", "q0", "b", "R")
   tm.add_transition("q0", "_", "OK", "_", "R")

   # Load and run
   tm.add_terminals("_")
   tm.set_tape(["a", "a", "a", "_"])
   while tm.register not in ("OK", "nOK"):
       tm.step()

   print(tm.tape)  # ['b', 'b', 'b', '_']

Linear Bounded Automaton — Type 1
----------------------------------

An LBA behaves like a Turing Machine with a bounded tape. Initialise it with
``tape_size`` to enforce the bound:

.. code-block:: python

   from fsm_tools import LinearBoundedAutomaton

   lba = LinearBoundedAutomaton(
       name="BoundedReplace",
       chomsky="Context-Sensitive",
       tape_size=[10],
       blank_symbol="_",
   )

   lba.add_terminals("a", "b", "_")
   lba.set_register("q0")
   lba.set_moves(R=[1], L=[-1])
   lba.add_transition("q0", "a", "OK", "b", "R")

   lba.set_tape(["a", "_"])
   lba.step()
   print(lba.tape)  # ['b', '_']

Pushdown Automaton — Type 2
----------------------------

Recognition of the context-free language :math:`L = \{a^nb^n \mid n \geq 1\}`:

.. code-block:: python

   from fsm_tools import PushdownAutomaton

   pda = PushdownAutomaton(
       name="anbn",
       stack_alphabet={"A"},
       bottom_symbol="Z",
   )

   pda.add_terminals("a", "b")
   pda.set_register("q0")
   pda.add_non_terminals("q1", "q2")

   # Transitions: (state_from, input_symbol, stack_top, state_to, stack_ops)
   pda.add_transition("q0", "a", "Z", "q0", ["A", "Z"])
   pda.add_transition("q0", "a", "A", "q0", ["A", "A"])
   pda.add_transition("q0", "b", "A", "q1", [])
   pda.add_transition("q1", "b", "A", "q1", [])
   pda.add_transition("q1", "b", "Z", "q2", [])

   print(pda.validate(["a", "b"]))           # True
   print(pda.validate(["a", "a", "b", "b"])) # True
   print(pda.validate(["a", "b", "b"]))      # False
   print(pda.validate([]))                    # False

.. note::

   :meth:`~fsm_tools.PushdownAutomaton.validate` resets the automaton
   (stack, register, input) before each run — it is safe to call multiple times
   on the same instance.

.. seealso::

   :doc:`usage` — error handling, API patterns, and stability notes.

   :doc:`/theory/chomsky/automata` — theoretical background for each automaton type.
