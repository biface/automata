"""
Extended automaton hierarchy for pedagogical purposes.

This module provides ``ExtendedTuringMachine`` and ``ExtendedLBA`` — subclasses
of the formal Chomsky hierarchy that demonstrate how a more expressive computational
model can be built within the same grammar classification.

Key principle: a richer tape structure (n-dimensional, bidirectional) does **not**
change the class of languages recognised. ``ExtendedTuringMachine`` still recognises
exactly the same Type 0 languages as ``TuringMachine``; ``ExtendedLBA`` still
recognises exactly the same Type 1 languages as ``LinearBoundedAutomaton``.
This is a direct illustration of the Church-Turing thesis.

Hierarchy::

    TuringMachine (advanced.py — 1D, formal)
    └── ExtendedTuringMachine   (n-D, dict-based infinite tape)
        └── ExtendedLBA         (n-D, dict-based bounded tape)
"""

from __future__ import annotations

from typing import Any, List

from .advanced import TuringMachine
from .exception import ReadError


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
