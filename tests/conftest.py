"""
Shared fixtures for the fsm-tools test suite.

Modules are loaded via ``importlib`` to:
  - Centralise import logic in one place.
  - Enable explicit testing of the public API surface.
  - Decouple test files from direct package imports.

Fixture scopes:
  - ``session`` — module-level objects loaded once per test run.
  - ``function`` — fresh automaton instances for each test.
"""

import importlib
import pytest


# ---------------------------------------------------------------------------
# Module fixtures (session-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def fsm_module():
    """Public API of fsm_tools — loaded via importlib."""
    return importlib.import_module("fsm_tools")


@pytest.fixture(scope="session")
def advanced_module():
    """fsm_tools.advanced — formal Chomsky hierarchy."""
    return importlib.import_module("fsm_tools.advanced")


@pytest.fixture(scope="session")
def extended_module():
    """fsm_tools.extended — pedagogical extended hierarchy."""
    return importlib.import_module("fsm_tools.extended")


@pytest.fixture(scope="session")
def exception_module():
    """fsm_tools.exception — exception hierarchy."""
    return importlib.import_module("fsm_tools.exception")


@pytest.fixture(scope="session")
def constants_module():
    """fsm_tools.constants — CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS."""
    return importlib.import_module("fsm_tools.constants")


# ---------------------------------------------------------------------------
# TuringMachine instances (function-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture
def tm_instance(fsm_module):
    """Standard 1D TuringMachine with F/B moves and register S."""
    return fsm_module.TuringMachine(
        "TestTM",
        axes=1,
        blank_symbol="_",
        movement={"F": [1], "B": [-1]},
        register="S",
        accept="OK",
        reject="nOK",
    )


@pytest.fixture
def tm_with_tape(tm_instance):
    """TuringMachine pre-loaded with symbols a, b, c on tape."""
    tm_instance.add_terminals("a", "b", "c")
    tm_instance.set_tape(["a", "b", "c"])
    return tm_instance


# ---------------------------------------------------------------------------
# LinearBoundedAutomaton instances (function-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture
def lba_instance(fsm_module):
    """LBA with tape limit 10, F/B moves, register S."""
    return fsm_module.LinearBoundedAutomaton(
        "TestLBA",
        tape_size=[10],
        axes=1,
        blank_symbol="_",
        movement={"F": [1], "B": [-1]},
        register="S",
        accept="OK",
        reject="nOK",
    )


@pytest.fixture
def lba_with_tape(lba_instance):
    """LBA pre-loaded with symbols a, b, c on tape."""
    lba_instance.add_terminals("a", "b", "c")
    lba_instance.set_tape(["a", "b", "c"])
    return lba_instance


# ---------------------------------------------------------------------------
# ExtendedTuringMachine instances (function-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture
def etm_instance(fsm_module):
    """ExtendedTuringMachine, 1D, F/B moves."""
    return fsm_module.ExtendedTuringMachine(
        "TestETM",
        axes=1,
        blank_symbol="_",
        movement={"F": [1], "B": [-1]},
        register="S",
        accept="OK",
        reject="nOK",
    )


@pytest.fixture
def etm_2d_instance(fsm_module):
    """ExtendedTuringMachine, 2D."""
    return fsm_module.ExtendedTuringMachine(
        "TestETM2D",
        axes=2,
        blank_symbol="_",
        register="S",
        accept="OK",
        reject="nOK",
    )


# ---------------------------------------------------------------------------
# ExtendedLBA instances (function-scoped)
# ---------------------------------------------------------------------------

@pytest.fixture
def elba_instance(fsm_module):
    """ExtendedLBA, 1D, tape limit 10."""
    return fsm_module.ExtendedLBA(
        "TestELBA",
        tape_size=[10],
        axes=1,
        blank_symbol="_",
        movement={"F": [1], "B": [-1]},
        register="S",
        accept="OK",
        reject="nOK",
    )


@pytest.fixture
def elba_2d_instance(fsm_module):
    """ExtendedLBA, 2D, tape limits [5, 5]."""
    return fsm_module.ExtendedLBA(
        "TestELBA2D",
        tape_size=[5, 5],
        axes=2,
        blank_symbol="_",
        register="S",
        accept="OK",
        reject="nOK",
    )
