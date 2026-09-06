"""
Extended automaton hierarchy for pedagogical purposes.

This module provides ``ExtendedTuringMachine``, ``ExtendedLBA`` and
``ExtendedPushdownAutomaton`` — subclasses of the formal Chomsky hierarchy
that demonstrate how a more expressive computational model can be built
within the same grammar classification.

Key principle: a richer tape structure (n-dimensional, bidirectional) does **not**
change the class of languages recognised. ``ExtendedTuringMachine`` still recognises
exactly the same Type 0 languages as ``TuringMachine``; ``ExtendedLBA`` still
recognises exactly the same Type 1 languages as ``LinearBoundedAutomaton``.
This is a direct illustration of the Church-Turing thesis. Likewise,
``ExtendedPushdownAutomaton``'s epsilon-transitions (#66, DD-013) are a
convenience for writing grammars, not an increase in recognising power —
every epsilon-PDA has an equivalent epsilon-free PDA.

Hierarchy::

    TuringMachine (advanced.py — 1D, formal)
    └── ExtendedTuringMachine   (n-D, dict-based infinite tape)
        └── ExtendedLBA         (n-D, dict-based bounded tape)

    PushdownAutomaton (advanced.py — no epsilon-transitions, formal)
    └── ExtendedPushdownAutomaton   (epsilon-transitions, epsilon-closure validate())
"""

from __future__ import annotations

from typing import Any, List

from .advanced import PushdownAutomaton, TuringMachine
from .exception import AddError, ReadError, SearchError, ValidationError


class ExtendedTuringMachine(TuringMachine):
    """
    A Turing Machine with an n-dimensional, bidirectionally infinite tape.

    ``ExtendedTuringMachine`` extends the canonical ``TuringMachine`` by lifting
    two constraints:

    - **Axes**: the tape may have any number of dimensions (``axes >= 1``).
    - **Direction**: the tape is infinite in all directions — the head may move
      to negative positions in any dimension.

    The tape is implemented as a dictionary mapping head position tuples to
    symbols, which naturally supports infinite extension in all directions
    without explicit memory management.

    Grammar classification: ``chomsky="Recursively Enumerable"`` (Type 0),
    inherited from ``TuringMachine``. The extended tape does not change the
    class of languages recognised.

    :param name: Name of the automaton.
    :type name: str
    :param axes: Number of tape dimensions. Must be >= 1. Defaults to 1.
    :type axes: int
    """

    def _validate_axes(self, axes: int) -> None:
        """
        Validates that the number of axes is at least 1.

        :param axes: Number of tape dimensions.
        :type axes: int
        :raises ValueError: If ``axes`` is less than 1.
        """
        if axes < 1:
            raise ValueError(f"ExtendedTuringMachine requires at least 1 axis. Got axes={axes}.")

    def __init__(
        self,
        name: str,
        axes: int = 1,
        blank_symbol: str = "_",
        movement: dict = None,
        register: str = "",
        accept: str = "OK",
        reject: str = "nOK",
        chomsky: str = "Recursively Enumerable",
    ):
        super().__init__(
            name,
            axes=axes,
            blank_symbol=blank_symbol,
            movement=movement,
            register=register,
            accept=accept,
            reject=reject,
            chomsky=chomsky,
        )
        # Replace the list-based tape with a dict-based infinite tape.
        # Keys are tuples of head coordinates; values are tape symbols.
        self.tape = {}
        self._TAPE_ALLOWS_NEGATIVE_POSITIONS = True

    def _extend_tape(self, location: list) -> None:
        """
        No-op: the dict-based tape is infinite by nature.

        The tape dictionary grows on demand in :meth:`read` and :meth:`write`.
        No pre-extension is required.

        :param location: Current head position (ignored).
        :type location: list
        """

    def read(self) -> Any:
        """
        Read the symbol at the current head position.

        Returns the blank symbol if the cell has not been written to.

        :return: Symbol at the current head position.
        :rtype: Any
        """
        return self.tape.get(tuple(self.head), self.blank)

    def write(self, symbol: Any) -> None:
        """
        Write a symbol at the current head position.

        If the symbol is not in the alphabet it is added automatically.

        :param symbol: Symbol to write.
        :type symbol: Any
        """
        if symbol not in self.grammar.alphabet:
            self.add_terminals(symbol)
        self.tape[tuple(self.head)] = symbol

    def set_tape(self, content: List[Any], location: List[int] = None) -> None:
        """
        Initialise the tape from a (possibly nested) list of symbols.

        A 1D tape is passed as a flat list: ``["a", "b", "c"]``.
        A 2D tape is passed as a list of rows: ``[["a", "b"], ["c", "d"]]``.
        The nesting depth must equal ``self.axes``.

        :param content: Symbols to load onto the tape.
        :type content: List[Any]
        :param location: Starting head position. Defaults to the origin.
        :type location: List[int] | None
        :raises ReadError: If any symbol is not in the alphabet.
        """

        def validate_and_load(data: Any, coords: list) -> None:
            if isinstance(data, list):
                for i, item in enumerate(data):
                    validate_and_load(item, coords + [i])
            else:
                if data not in self.get_terminals():
                    raise ReadError(self.GRAMMAR, "alphabet", symbol=data)
                self.tape[tuple(coords)] = data

        self.tape = {}
        validate_and_load(content, [])
        self.head = location if location is not None else [0] * self.axes


class ExtendedLBA(ExtendedTuringMachine):
    """
    A Linear Bounded Automaton with an n-dimensional bounded tape.

    ``ExtendedLBA`` subclasses ``ExtendedTuringMachine`` and reintroduces the
    tape size limits of the Linear Bounded Automaton, applied independently
    to each dimension of the n-D tape.

    Like ``ExtendedTuringMachine``, it uses a dict-based tape. The head is
    blocked — with an ``IndexError`` — if it reaches a boundary in any dimension.

    Grammar classification: ``chomsky="Context-Sensitive"`` (Type 1). The bounded
    tape restricts the class of languages recognised relative to
    ``ExtendedTuringMachine``, exactly as in the formal Chomsky hierarchy.

    :param name: Name of the automaton.
    :type name: str
    :param tape_size: Maximum tape size for each dimension.
    :type tape_size: List[int]
    :param axes: Number of tape dimensions. Must match ``len(tape_size)``.
    :type axes: int
    """

    def __init__(
        self,
        name: str,
        tape_size: List[int],
        axes: int = 1,
        blank_symbol: str = "_",
        movement: dict = None,
        register: str = "",
        accept: str = "OK",
        reject: str = "nOK",
    ):
        super().__init__(
            name,
            axes=axes,
            blank_symbol=blank_symbol,
            movement=movement,
            register=register,
            accept=accept,
            reject=reject,
            chomsky="Context-Sensitive",
        )
        if len(tape_size) != self.axes:
            raise ValueError(
                f"tape_size must contain exactly {self.axes} value(s) "
                f"(one per dimension). Got {len(tape_size)}."
            )
        self.limits = tape_size

    def _extend_tape(self, location: list) -> None:
        """
        Checks that the head is within bounds for each dimension.

        :param location: Current head position.
        :type location: list
        :raises IndexError: If the head exceeds the tape limit in any dimension.
        """
        for i, pos in enumerate(location):
            if abs(pos) >= self.limits[i]:
                raise IndexError(
                    f"Head position {pos} in dimension {i} exceeds the tape "
                    f"limit of {self.limits[i]}."
                )

    def read(self) -> Any:
        """
        Read the symbol at the current head position, enforcing tape bounds.

        :return: Symbol at the current head position.
        :rtype: Any
        :raises IndexError: If the head is out of bounds.
        """
        self._extend_tape(self.head)
        return self.tape.get(tuple(self.head), self.blank)

    def write(self, symbol: Any) -> None:
        """
        Write a symbol at the current head position, enforcing tape bounds.

        :param symbol: Symbol to write.
        :type symbol: Any
        :raises IndexError: If the head is out of bounds.
        """
        self._extend_tape(self.head)
        if symbol not in self.grammar.alphabet:
            self.add_terminals(symbol)
        self.tape[tuple(self.head)] = symbol

    def set_tape(self, content: List[Any], location: List[int] = None) -> None:
        """
        Initialise the tape from a (possibly nested) list of symbols,
        validating content against the dimension limits.

        :param content: Symbols to load onto the tape.
        :type content: List[Any]
        :param location: Starting head position. Defaults to the origin.
        :type location: List[int] | None
        :raises ValueError: If content in any dimension exceeds its limit.
        :raises ReadError: If any symbol is not in the alphabet.
        """

        def validate_and_load(data: Any, coords: list) -> None:
            if isinstance(data, list):
                dim = len(coords)
                if dim < self.axes and len(data) > self.limits[dim]:
                    raise ValueError(
                        f"Content length {len(data)} in dimension {dim} "
                        f"exceeds tape limit {self.limits[dim]}."
                    )
                for i, item in enumerate(data):
                    validate_and_load(item, coords + [i])
            else:
                if data not in self.get_terminals():
                    raise ReadError(self.GRAMMAR, "alphabet", symbol=data)
                self.tape[tuple(coords)] = data

        self.tape = {}
        validate_and_load(content, [])
        self.head = location if location is not None else [0] * self.axes


class ExtendedPushdownAutomaton(PushdownAutomaton):
    """
    Pedagogical extension of PushdownAutomaton (DD-012 pattern) lifting the
    v0.1.0 restriction on epsilon-transitions (DD-013, #64). A rule with
    ``input_symbol=None`` may fire without consuming input.

    Epsilon-transitions make the automaton genuinely non-deterministic: at a
    given (state, stack top), an epsilon-transition and a symbol-consuming
    transition can both be applicable at once, and choosing the wrong one
    first can lead to a dead end even though a valid accepting path exists.
    ``PushdownAutomaton.step()``/``validate()`` are deterministic, single-path
    (DD-013) — correct for a PDA with no epsilon-transitions, where at most
    one rule can ever match a given configuration, but insufficient here.

    ``validate()`` is therefore replaced with a breadth-first search over
    reachable configurations ``(state, input_pos, stack)`` rather than a
    linear walk, exploring every applicable transition (epsilon and
    symbol-consuming) at each configuration instead of committing to the
    first match. ``step()`` keeps its single-transition, first-match
    semantics for direct/manual use, extended only to allow epsilon rules
    to fire without advancing ``input_pos``.
    """

    def add_transition(
        self,
        state_from: Any,
        input_symbol: Any,
        stack_top: Any,
        state_to: Any,
        stack_ops: List[Any],
    ) -> None:
        """
        Same contract as ``PushdownAutomaton.add_transition``, except that
        ``input_symbol=None`` (an epsilon-transition) is accepted instead of
        raising ``NotImplementedError``.

        :raises ReadError: If ``input_symbol`` is not ``None`` and not in the
            input alphabet, or ``stack_top`` / any symbol in ``stack_ops`` is
            not in the stack alphabet.
        :raises AddError: If an identical transition already exists.
        """
        if input_symbol is not None and input_symbol not in self.get_terminals():
            raise ReadError(self.GRAMMAR, "alphabet", symbol=input_symbol)

        if stack_top not in self.stack_alphabet:
            raise AddError(self.GRAMMAR, "stack", symbol=stack_top)

        for sym in stack_ops:
            if sym not in self.stack_alphabet:
                raise AddError(self.GRAMMAR, "stack", symbol=sym)

        for state in (state_from, state_to):
            if state not in self.grammar.states:
                self.add_non_terminals(state)

        rule = (state_from, input_symbol, stack_top, state_to, stack_ops)
        if rule in self.grammar.rules:
            raise AddError(self.GRAMMAR, "transitions", transition=str(rule))
        self.add_rules(rule)

    def step(self) -> None:
        """
        Apply the first rule matching the current configuration — an
        epsilon-transition (``input_symbol=None``, stack top only) or a
        symbol-consuming one — preferring epsilon-transitions first so a
        direct/manual call always makes progress on the stack when one is
        available. Epsilon-transitions do not advance ``input_pos``.

        :raises SearchError: If no rule matches the current configuration.
        """
        current_input = self._current_input()
        current_top = self.peek()

        for rule in self.grammar.rules:
            state_from, input_symbol, stack_top, state_to, stack_ops = rule
            if self.register == state_from and input_symbol is None and current_top == stack_top:
                self.pop()
                for sym in reversed(stack_ops):
                    self.push(sym)
                self.register = state_to
                return

        for rule in self.grammar.rules:
            state_from, input_symbol, stack_top, state_to, stack_ops = rule
            if (
                self.register == state_from
                and current_input == input_symbol
                and current_top == stack_top
            ):
                self.pop()
                for sym in reversed(stack_ops):
                    self.push(sym)
                self.input_pos += 1
                self.register = state_to
                return

        raise SearchError(
            self.GRAMMAR,
            "grammar",
            reason=(
                f"no rule for state='{self.register}', "
                f"input='{current_input}', stack_top='{current_top}'"
            ),
        )

    def validate(self, word: List[Any]) -> bool:
        """
        Accept ``word`` if any epsilon-closure-aware path through the
        transition relation ends with the whole word consumed and the stack
        reduced to the bottom marker (empty-stack acceptance, DD-013).

        Explores configurations breadth-first rather than committing to a
        single path, since an epsilon-transition and a symbol-consuming
        transition can both be applicable at once. A ``(state, input_pos,
        stack)`` visited set prevents infinite loops through epsilon cycles.

        :param word: Sequence of input symbols to validate.
        :type word: List[Any]
        :return: ``True`` if any explored path accepts, ``False`` otherwise.
        :rtype: bool
        :raises ValidationError: If the automaton is not configured to
            validate at all (no start state, no alphabet, no transitions).
        """
        if self.grammar.start is None:
            raise ValidationError(self.GRAMMAR, "validation", reason="no start state defined")
        if not self.grammar.alphabet:
            raise ValidationError(self.GRAMMAR, "validation", reason="no input alphabet defined")
        if not self.grammar.rules:
            raise ValidationError(self.GRAMMAR, "validation", reason="no transitions defined")

        start_config = (self.grammar.start, 0, (self.bottom_symbol,))
        frontier = [start_config]
        visited = {start_config}

        while frontier:
            state, pos, stack = frontier.pop()
            if not stack:
                continue  # dead end: no top symbol left, no rule can ever match again
            stack_top = stack[-1]

            for state_from, input_symbol, top, state_to, stack_ops in self.grammar.rules:
                if state_from != state or top != stack_top:
                    continue

                if input_symbol is None:
                    new_pos = pos
                elif pos < len(word) and word[pos] == input_symbol:
                    new_pos = pos + 1
                else:
                    continue

                new_stack = stack[:-1] + tuple(reversed(stack_ops))
                new_config = (state_to, new_pos, new_stack)

                if new_pos == len(word) and new_stack == (self.bottom_symbol,):
                    return True

                if new_config not in visited:
                    visited.add(new_config)
                    frontier.append(new_config)

        return False
