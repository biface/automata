# Contributing to fsm-tools

Thank you for your interest in contributing. This document explains how to set up
the development environment and how to submit changes.

---

## Prerequisites

- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) for environment and package management
- [tox](https://tox.wiki/) + [tox-uv](https://github.com/tox-dev/tox-uv) for
  multi-version test orchestration
- PyCharm is the recommended IDE, but any editor works

---

## Setting up the environment

```bash
git clone https://github.com/biface/automata.git
cd automata
uv sync --extra dev
```

---

## Running the checks locally

Individual tools:

```bash
uv run ruff check src/ tests/          # lint
uv run mypy src/fsm_tools              # type check
uv run pytest --tb=short               # tests
uv run pytest --cov=fsm_tools          # tests with coverage
```

Full matrix across Python 3.10, 3.11 and 3.12 via tox:

```bash
tox                    # run all environments
tox -e lint            # Ruff only
tox -e type            # MyPy only
tox -e py310           # pytest on Python 3.10
tox -e py311           # pytest on Python 3.11
tox -e py312           # pytest on Python 3.12
```

All tox environments must pass before opening a pull request.

---

## Branch naming

```
type/short-description
```

Examples:
- `feat/pushdown-automaton`
- `fix/tape-extension-lba`
- `chore/update-ruff`
- `docs/theory-pages`

---

## Commit messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): short description

Optional body explaining the why, not the what.

Closes #42
```

Types: `feat`, `fix`, `docs`, `chore`, `ci`, `test`, `refactor`, `perf`, `style`.

---

## Opening a pull request

1. Create a branch from `master`
2. Make your changes — keep the scope focused
3. Ensure all tox environments pass
4. Open a pull request on GitHub with:
   - A clear title following the commit convention
   - A description explaining the motivation and approach
   - A reference to the related issue (`Closes #xx`)

---

## Design decisions

Significant architectural choices are tracked as
[`type: decision` issues on GitHub](https://github.com/biface/automata/issues?q=label%3A%22type%3A+decision%22),
numbered `DD-xxx`. Each decision is discussed and validated with the maintainers
before any implementation begins. Accepted decisions produce one or more operational
issues that define the concrete work to be done.

If your contribution involves an architectural choice, open a `type: decision` issue
first, discuss it with the maintainers, and reference the validated decision in any
subsequent pull request.

---

## Deprecation policy

No breaking changes are permitted without a major version bump from v0.6.0 onwards.
Deprecation warnings must be added at least one minor version before removal.

---

## Code of conduct

All contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
