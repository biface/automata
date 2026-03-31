# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.0.2] — 2026-05-09

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

[Unreleased]: https://github.com/biface/automata/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/biface/automata/compare/v0.0.1...v0.0.2
