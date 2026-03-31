# Contribuer à fsm-tools

Merci de votre intérêt pour le projet. Ce document explique comment configurer
l'environnement de développement et soumettre des modifications.

---

## Prérequis

- Python 3.10 ou supérieur
- [uv](https://github.com/astral-sh/uv) pour la gestion de l'environnement et des paquets
- [tox](https://tox.wiki/) + [tox-uv](https://github.com/tox-dev/tox-uv) pour
  l'orchestration des tests sur plusieurs versions Python
- PyCharm est l'IDE recommandé, mais tout éditeur convient

---

## Mise en place de l'environnement

```bash
git clone https://github.com/biface/automata.git
cd automata
uv sync --extra dev
```

---

## Lancer les vérifications en local

Outils individuels :

```bash
uv run ruff check src/ tests/          # lint
uv run mypy src/fsm_tools              # vérification des types
uv run pytest --tb=short               # tests
uv run pytest --cov=fsm_tools          # tests avec couverture
```

Matrice complète sur Python 3.10, 3.11 et 3.12 via tox :

```bash
tox                    # lancer tous les environnements
tox -e lint            # Ruff uniquement
tox -e type            # MyPy uniquement
tox -e py310           # pytest sur Python 3.10
tox -e py311           # pytest sur Python 3.11
tox -e py312           # pytest sur Python 3.12
```

Tous les environnements tox doivent passer avant d'ouvrir une pull request.

---

## Nommage des branches

```
type/description-courte
```

Exemples :
- `feat/automate-a-pile`
- `fix/extension-bande-lba`
- `chore/mise-a-jour-ruff`
- `docs/pages-theorie`

---

## Messages de commit

Suivre le format [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```
type(scope): description courte

Corps optionnel expliquant le pourquoi, pas le quoi.

Closes #42
```

Types : `feat`, `fix`, `docs`, `chore`, `ci`, `test`, `refactor`, `perf`, `style`.

---

## Ouvrir une pull request

1. Créez une branche depuis `master`
2. Apportez vos modifications — gardez un périmètre ciblé
3. Vérifiez que tous les environnements tox passent
4. Ouvrez une pull request sur GitHub avec :
   - Un titre clair suivant la convention de commit
   - Une description expliquant la motivation et l'approche
   - Une référence à l'issue concernée (`Closes #xx`)

---

## Décisions de conception

Les choix architecturaux significatifs sont suivis comme
[issues `type: decision` sur GitHub](https://github.com/biface/automata/issues?q=label%3A%22type%3A+decision%22),
numérotées `DD-xxx`. Chaque décision est discutée et validée avec les mainteneurs
avant tout début d'implémentation. Les décisions acceptées donnent lieu à une ou
plusieurs issues opérationnelles qui définissent le travail concret à réaliser.

Si votre contribution implique un choix architectural, ouvrez d'abord une issue
`type: decision`, discutez-la avec les mainteneurs, et référencez la décision validée
dans toute pull request qui en découle.

---

## Politique de dépréciation

Aucune modification non rétrocompatible n'est permise sans une montée de version majeure
à partir de v0.6.0. Les avertissements de dépréciation doivent être ajoutés au moins
une version mineure avant la suppression.

---

## Code de conduite

Tous les contributeurs sont tenus de respecter le
[Code de Conduite](CODE_DE_CONDUITE.md).
