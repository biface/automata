![Python](https://img.shields.io/badge/Language-Python-green.svg)
![CI](https://github.com/biface/automata/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/biface/automata/branch/master/graph/badge.svg)](https://codecov.io/gh/biface/automata)
[![PyPI](https://img.shields.io/pypi/v/fsm-tools.svg)](https://pypi.org/project/fsm-tools/)

*[Read in English](README.md)*

---

# fsm-tools

Une bibliothèque Python formelle pour la modélisation des automates de la hiérarchie de Chomsky.

## Vue d'ensemble

**fsm-tools** fournit une implémentation rigoureuse des quatre familles d'automates
définies par la hiérarchie des grammaires et des langages de Chomsky :

| Type | Automate | Famille de langages |
|------|----------|---------------------|
| 0 | `TuringMachine` | Récursivement énumérables |
| 1 | `LinearBoundedAutomaton` | Contextuels |
| 2 | `PushdownAutomaton` | Hors-contexte |
| 3 | `FiniteStateAutomaton` | Rationnels |

Chaque classe est une restriction formelle de celle qui la précède — elle hérite de
sa structure et la contraint davantage. La hiérarchie est implémentée comme une chaîne
d'héritage stricte :

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

## Démarrage rapide

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

## Documentation

La documentation complète est disponible sur
[fsm-tools.readthedocs.io](https://fsm-tools.readthedocs.io).

## Liens

- [PyPI](https://pypi.org/project/fsm-tools/)
- [GitHub](https://github.com/biface/automata)
- [Issues](https://github.com/biface/automata/issues)
- [Contribuer](CONTRIBUTING.fr.md)
- [Changelog](CHANGELOG.md)

## Licence

Ce projet est distribué sous la licence
[CeCILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html).
La version française est la référence juridiquement opposable — voir [LICENSE.fr](LICENSE.fr).
