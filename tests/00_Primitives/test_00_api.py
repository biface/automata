"""
Public API structure tests.

Verifies that ``fsm_tools.__init__`` correctly exposes both the formal
Chomsky hierarchy (advanced.py) and the extended hierarchy (extended.py),
as well as the full exception hierarchy and version string.

All imports use ``importlib`` to test the package surface as an external
consumer would discover it.
"""

import importlib


class TestPublicAPIClasses:

    def test_formal_hierarchy_exported(self, fsm_module):
        """All formal Chomsky hierarchy classes are accessible from fsm_tools."""
        for name in ("Grammar", "Automaton", "TuringMachine", "LinearBoundedAutomaton"):
            assert hasattr(fsm_module, name), f"Missing: {name}"

    def test_extended_hierarchy_exported(self, fsm_module):
        """Extended hierarchy classes are accessible from fsm_tools."""
        for name in ("ExtendedTuringMachine", "ExtendedLBA"):
            assert hasattr(fsm_module, name), f"Missing: {name}"

    def test_exception_hierarchy_exported(self, fsm_module):
        """All exception classes are accessible from fsm_tools."""
        for name in (
            "AutomatonException", "AutomatonError", "AutomatonGroup",
            "ReadError", "AddError", "RemoveError", "ModifyError",
            "ValidationError", "SearchError", "RemoveComponentError",
        ):
            assert hasattr(fsm_module, name), f"Missing: {name}"

    def test_version_exported(self, fsm_module):
        """__VERSION__ is present and is a non-empty string."""
        assert hasattr(fsm_module, "__VERSION__")
        assert isinstance(fsm_module.__VERSION__, str)
        assert len(fsm_module.__VERSION__) > 0


class TestPublicAPIOrigins:

    def test_turing_machine_from_advanced(self, fsm_module, advanced_module):
        """TuringMachine exported from fsm_tools is the same as in advanced."""
        assert fsm_module.TuringMachine is advanced_module.TuringMachine

    def test_lba_from_advanced(self, fsm_module, advanced_module):
        """LinearBoundedAutomaton exported from fsm_tools is from advanced."""
        assert fsm_module.LinearBoundedAutomaton is advanced_module.LinearBoundedAutomaton

    def test_extended_tm_from_extended(self, fsm_module, extended_module):
        """ExtendedTuringMachine exported from fsm_tools is from extended."""
        assert fsm_module.ExtendedTuringMachine is extended_module.ExtendedTuringMachine

    def test_extended_lba_from_extended(self, fsm_module, extended_module):
        """ExtendedLBA exported from fsm_tools is from extended."""
        assert fsm_module.ExtendedLBA is extended_module.ExtendedLBA


class TestPublicAPIHierarchy:

    def test_tm_is_automaton(self, fsm_module):
        """TuringMachine is a subclass of Automaton."""
        assert issubclass(fsm_module.TuringMachine, fsm_module.Automaton)

    def test_lba_is_tm(self, fsm_module):
        """LinearBoundedAutomaton is a subclass of TuringMachine."""
        assert issubclass(fsm_module.LinearBoundedAutomaton, fsm_module.TuringMachine)

    def test_extended_tm_is_tm(self, fsm_module):
        """ExtendedTuringMachine is a subclass of TuringMachine."""
        assert issubclass(fsm_module.ExtendedTuringMachine, fsm_module.TuringMachine)

    def test_extended_lba_is_extended_tm(self, fsm_module):
        """ExtendedLBA is a subclass of ExtendedTuringMachine."""
        assert issubclass(fsm_module.ExtendedLBA, fsm_module.ExtendedTuringMachine)

    def test_extended_lba_is_not_lba(self, fsm_module):
        """ExtendedLBA is NOT a subclass of LinearBoundedAutomaton (Option C — DD-012)."""
        assert not issubclass(fsm_module.ExtendedLBA, fsm_module.LinearBoundedAutomaton)

    def test_chomsky_grammar_on_tm(self, fsm_module):
        """TuringMachine instances carry Recursively Enumerable classification."""
        tm = fsm_module.TuringMachine("T", register="S")
        assert tm.GRAMMAR == "Recursively Enumerable"

    def test_chomsky_grammar_on_extended_lba(self, fsm_module):
        """ExtendedLBA instances carry Context-Sensitive classification."""
        elba = fsm_module.ExtendedLBA("E", tape_size=[5], register="S")
        assert elba.GRAMMAR == "Context-Sensitive"


class TestImportlibReload:

    def test_submodules_independently_importable(self):
        """advanced and extended are importable as standalone submodules."""
        adv = importlib.import_module("fsm_tools.advanced")
        ext = importlib.import_module("fsm_tools.extended")
        assert hasattr(adv, "TuringMachine")
        assert hasattr(ext, "ExtendedTuringMachine")
