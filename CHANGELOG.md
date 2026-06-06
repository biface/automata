# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.0] — 2026-06-06

First PyPI publication — Pre-Alpha release.

### Added

- `PushdownAutomaton` (Type 2 — Context-Free) in `advanced.py` (#26)
  - Stack-based memory model: `push`, `pop`, `peek`, `reset_stack`
  - Separate stack alphabet distinct from the input alphabet
  - Transition 5-tuple: `(state_from, input_symbol, stack_top, state_to, stack_ops)`
  - Acceptance by empty stack (bottom marker convention)
  - Epsilon-transitions reserved for v0.3.0 (`NotImplementedError`)
  - Tape-based inherited methods overridden to `NotImplementedError`
- `test_07_pushdown_automaton.py` — 35 tests, aⁿbⁿ recogniser (#26)
- `Grammar.start` annotated as `Optional[Any]` for basedpyright compliance

### Changed

- `__init__.py`: exports `PushdownAutomaton`, version bumped to `0.1.0`
- `README.md` and `README.fr.md` rewritten for v0.1.0 (#27):
  - Badge CI corrected to `ci-tests.yml`
  - Implementation status column added to the hierarchy table
  - Quick start extended with a `PushdownAutomaton` example
- `pyproject.toml`: version `0.1.0`, classifier updated to
  `Development Status :: 2 - Pre-Alpha`
- Exception codes on stack operations aligned with existing JSON message IDs:
  `AddError("stack")` for invalid symbols, `RemoveComponentError("stack")` for
  empty stack access
- `validate()`: rejects the empty word explicitly; accepts when stack equals
  `[bottom_symbol]`
- `set_register` and `add_transition` in `PushdownAutomaton` annotated with
  `# type: ignore[override]` (incompatible override resolved at v0.5.0)

---

## [0.0.5] — 2026-05-29

### Added

- GitHub issue templates: bug report, feature request, decision (DD), question (#46)
- GitHub pull request template (#47)
- `.codecov.yml` and `source_pkgs` coverage fix (#48)
- Pre-release CI workflow `publish.yml` (TestPyPI → PyPI, OIDC trusted publishing) (#50)
- Dependabot configuration for GitHub Actions and pip dependencies (#51)

### Changed

- `tox -e lint` and `tox -e type` environments fixed (#49)
- CI matrix restricted to Linux (`ubuntu-latest`) — Windows/macOS deferred to v0.0.5+

---

## [0.0.4] — 2026-05-10

### Added

- `extended.py`: `ExtendedTuringMachine` and `ExtendedLBA` — pedagogical n-dimensional
  tape extensions (DD-012, #23, #54)
- `TuringMachine._extend_tape` implemented for 1D tapes (#23)
- `LinearBoundedAutomaton.set_tape` dimension bug fixed (#24)
- `test_06_turing_machine.py` extended — coverage ≥ 80% on TM and LBA (#25)
- `__init__.py` exports `ExtendedTuringMachine` and `ExtendedLBA`

### Changed

- `TuringMachine`: `axes` constrained to 1; `_extend_tape` now dynamically
  extends the tape with blank symbols in both directions (#23)
- `LinearBoundedAutomaton.set_tape`: correctly compares content length against
  limits per dimension, not per symbol (#24)

---

## [0.0.3] — 2026-04-06

### Added

- `test_00_exceptions_messages.py` — en-US fixed message system, replaces
  locale-switching tests (#22)

### Changed

- `utils/json.py`: locale dispatch removed, language fixed to `en-US`;
  `lang: str = None` parameter kept for future `i18n-tools` compatibility (#21)
- `AutomatonException` docstring updated: `locale` parameter is a no-op
  until `i18n-tools` is integrated (#21)
- `test_00_errors_locales.py` renamed to `test_00_exceptions_messages.py`;
  all locale-switching assertions replaced by en-US assertions (#22)

### Removed

- `src/fsm_tools/utils/i18n.py` — gettext-based message system (#19)
- All `.mo` compiled binary files from `locales/` (#19)
- `json_to_po()` utility function — tied to removed gettext infrastructure (#21)

---

## [0.0.2] — 2026-03-31

### Added

- GitHub Actions CI workflows: `lint.yml` (Ruff), `test.yml` (pytest + Codecov,
  matrix Python 3.10/3.11/3.12 × Ubuntu/Windows/macOS), `typecheck.yml` (MyPy)
- GitHub-to-GitLab push mirror workflow (`mirror.yml`)
- `tox.ini` with `tox-uv` for local multi-version test orchestration
- `CONTRIBUTING.md` and `CONTRIBUTING.fr.md`
- `CODE_OF_CONDUCT.md` and `CODE_DE_CONDUITE.md`
- `CHANGELOG.md` (this file)
- `test_automaton_requires_chomsky()` — explicit test for mandatory `chomsky` parameter

### Changed

- `pyproject.toml` fully overhauled: version `0.0.2`, `requires-python = ">=3.10"`,
  classifiers updated, URLs corrected, tool sections added (pytest, coverage, mypy, ruff)
- `Automaton.__init__`: `chomsky` is now a mandatory keyword-only parameter —
  omitting it raises `TypeError`
- `README.md` rewritten for the formal Chomsky scope; split into `README.md` (EN)
  and `README.fr.md` (FR)
- Development environment migrated from `virtualenv` to `uv`

### Removed

- `src/fsm_tools/lightweight.py` — lightweight FSM layer (see DD-001)
- `src/fsm_tools/django.py` — Django integration layer (deferred to `django-automata`)
- `src/cli/`, `src/gui/`, `src/utils/modelisation/`, `src/pychrom.py` — obsolete modules
- `tests/test_01_class_FSM.py`, `tests/test_02_class_extFSM.py`,
  `tests/test_03_class_contextFSM.py` — tests for removed modules
- Orphaned `empty_automaton` fixture from `test_05_class_automaton.py`
- `LICENSE.md` replaced by `LICENSE` (full CeCILL-C EN text) and `LICENSE.fr`

---

[Unreleased]: https://github.com/biface/automata/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/biface/automata/compare/v0.0.5...v0.1.0
[0.0.5]: https://github.com/biface/automata/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/biface/automata/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/biface/automata/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/biface/automata/compare/v0.0.1...v0.0.2
