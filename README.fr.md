![Python](https://img.shields.io/badge/Language-Python-green.svg)
![CI](https://github.com/biface/automata/actions/workflows/ci-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/biface/automata/branch/master/graph/badge.svg)](https://codecov.io/gh/biface/automata)
[![PyPI](https://img.shields.io/pypi/v/fsm-tools.svg)](https://pypi.org/project/fsm-tools/)

*[Read in English](README.md)*

---

# fsm-tools

Une bibliothèque Python formelle pour la modélisation des automates de la hiérarchie de Chomsky.

## Vue d'ensemble

**fsm-tools** fournit une implémentation rigoureuse des quatre familles d'automates
définies par la hiérarchie des grammaires et des langages de Chomsky :

| Type  | Automate                 | Famille de langages       | État            |
|-------|--------------------------|---------------------------|-----------------|
| 0     | `TuringMachine`          | Récursivement énumérables | ✅ v0.0.4        |
| 1     | `LinearBoundedAutomaton` | Contextuels               | ✅ v0.0.4        |
| 2     | `PushdownAutomaton`      | Hors-contexte             | ✅ v0.1.0        |
| 3     | `FiniteStateAutomaton`   | Rationnels                | 🔄 prévu v0.2.0 |

Chaque classe est une restriction formelle de celle qui la précède — elle hérite de
sa structure et la contraint davantage. La hiérarchie est implémentée comme une chaîne
d'héritage stricte :

```
Automaton
└── TuringMachine               (Type 0)
    └── LinearBoundedAutomaton  (Type 1)
        └── PushdownAutomaton   (Type 2)
            └── FiniteStateAutomaton  (Type 3 — prévu v0.2.0)
```

## Installation

```bash
pip install fsm-tools
```

## Démarrage rapide

### Machine de Turing (Type 0)

```python
from fsm_tools import TuringMachine

tm = TuringMachine(
    name="IncrementBinaire",
    chomsky="Recursively Enumerable",
    axes=1,
    blank_symbol="_",
    movement={"R": [1], "L": [-1]},
    register="q0",
    accept="qAccept",
    reject="qReject",
)
```

### Automate à pile (Type 2)

Reconnaissance du langage hors-contexte L = { aⁿbⁿ | n ≥ 1 } :

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

La documentation complète est disponible sur
[fsm-tools.readthedocs.io](https://fsm-tools.readthedocs.io).

## Liens

- [PyPI](https://pypi.org/project/fsm-tools/)
- [GitHub](https://github.com/biface/automata)\n- [Issues](https://github.com/biface/automata/issues)
- [Contribuer](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Licence

Ce projet est distribué sous la licence
[CeCILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html).
La version française est la référence juridiquement opposable — voir [LICENSE.fr](LICENSE.fr).
