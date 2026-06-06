![Python](https://img.shields.io/badge/Language-Python-green.svg)
![CI](https://github.com/biface/automata/actions/workflows/ci-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/biface/automata/branch/master/graph/badge.svg)](https://codecov.io/gh/biface/automata)
[![PyPI](https://img.shields.io/pypi/v/fsm-tools.svg)](https://pypi.org/project/fsm-tools/)

*[Lire en français](README.fr.md)*

---

# fsm-tools

A formal Python library for modelling automata in the Chomsky hierarchy.

## Overview

**fsm-tools** provides a rigorous implementation of the four automaton families
defined by Chomsky's grammar and language hierarchy:

| Type  | Automaton                | Language family        | Status            |
|-------|--------------------------|------------------------|-------------------|
| 0     | `TuringMachine`          | Recursively enumerable | ✅ v0.0.4          |
| 1     | `LinearBoundedAutomaton` | Context-sensitive      | ✅ v0.0.4          |
| 2     | `PushdownAutomaton`      | Context-free           | ✅ v0.1.0          |
| 3     | `FiniteStateAutomaton`   | Regular                | 🔄 planned v0.2.0 |

Each class is a formal restriction of the one above it — inheriting its structure
and constraining it further. The hierarchy is implemented as a strict inheritance
chain:

```
Automaton
└── TuringMachine               (Type 0)
    └── LinearBoundedAutomaton  (Type 1)
        └── PushdownAutomaton   (Type 2)
            └── FiniteStateAutomaton  (Type 3 — planned v0.2.0)
```

## Installation

```bash
pip install fsm-tools
```

## Quick start

### Turing Machine (Type 0)

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

### Pushdown Automaton (Type 2)

Recognition of the context-free language L = { aⁿbⁿ | n ≥ 1 }:

```python
from fsm_tools import PushdownAutomaton

pda = PushdownAutomaton(
    name="anbn",
    stack_alphabet={"A"},
    bottom_symbol="Z",
)
pda.add_terminals("a", "b")
pda.set_register("q0")
pda.add_non_terminals("q1", "q2")

pda.add_transition("q0", "a", "Z", "q0", ["A", "Z"])
pda.add_transition("q0", "a", "A", "q0", ["A", "A"])
pda.add_transition("q0", "b", "A", "q1", [])
pda.add_transition("q1", "b", "A", "q1", [])
pda.add_transition("q1", "b", "Z", "q2", [])

pda.validate(["a", "b"])        # True
pda.validate(["a", "a", "b"])   # False
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
