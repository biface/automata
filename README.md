![Python](https://img.shields.io/badge/Language-Python-green.svg)
![CI](https://github.com/biface/automata/actions/workflows/python-ci-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/biface/automata/branch/master/graph/badge.svg)](https://codecov.io/gh/biface/automata)
[![PyPI](https://img.shields.io/pypi/v/fsm-tools.svg)](https://pypi.org/project/fsm-tools/)

*[Lire en français](README.fr.md)*

---

# fsm-tools

A formal Python library for modelling automata in the Chomsky hierarchy.

## Overview

**fsm-tools** provides a rigorous implementation of the four automaton families
defined by Chomsky's grammar and language hierarchy:

| Type | Automaton | Language family |
|------|-----------|-----------------|
| 0 | `TuringMachine` | Recursively enumerable |
| 1 | `LinearBoundedAutomaton` | Context-sensitive |
| 2 | `PushdownAutomaton` | Context-free |
| 3 | `FiniteStateAutomaton` | Regular |

Each class is a formal restriction of the one above it — inheriting its structure
and constraining it further. The hierarchy is implemented as a strict inheritance
chain:

```
Automaton
└── TuringMachine               (Type 0)
    └── LinearBoundedAutomaton  (Type 1)
        └── PushdownAutomaton   (Type 2)
            └── FiniteStateAutomaton  (Type 3)
```

## Installation

```bash
pip install fsm-tools
```

## Quick start

```python
from fsm_tools import TuringMachine

tm = TuringMachine(
    name="BinaryIncrement",
    chomsky="Recursively Enumerable",
    axes=1,
    blank_symbol="_",
    movement={"R": [1], "L": [-1]},
    register="q0",
    accept="qAccept",
    reject="qReject",
)
```

## Documentation

Full documentation is available at
[fsm-tools.readthedocs.io](https://fsm-tools.readthedocs.io).

## Links

- [PyPI](https://pypi.org/project/fsm-tools/)
- [GitHub](https://github.com/biface/automata)
- [Issues](https://github.com/biface/automata/issues)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

This project is licensed under the
[CeCILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html) license.
The French version is the legally authoritative reference — see [LICENSE.fr](LICENSE.fr).
