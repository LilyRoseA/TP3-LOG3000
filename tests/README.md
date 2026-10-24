# `tests/` — Suite de tests

## Raison d'être

Ce répertoire contient les tests automatisés du projet, écrits avec
[pytest](https://docs.pytest.org/). Ils vérifient que le backend calcule
correctement, que la route Flask gère les erreurs et que l'interface affiche
les bons boutons. Les valeurs attendues suivent le comportement documenté dans
les docstrings du code, et non le comportement actuel : un test qui échoue
signale un bogue.

## Exécuter les tests

Depuis la racine du projet, environnement virtuel activé et dépendances
installées (`python -m pip install -r requirements.txt`) :

```bash
python -m pytest                              # toute la suite
python -m pytest -v                           # détail de chaque test
python -m pytest tests/test_operators.py      # un seul fichier
python -m pytest -k subtract                  # tests dont le nom contient « subtract »
python -m pytest -rf                          # résumé des tests échoués à la fin
```

La configuration se trouve dans `pytest.ini` à la racine : elle limite la
découverte à `tests/` et ajoute la racine au chemin d'import, pour que les
tests puissent faire `import app` et `import operators`. La commande `pytest`
seule fonctionne donc aussi.

Aucun serveur n'a besoin d'être lancé : les tests de route utilisent le
client de test de Flask.

## Fichiers et couverture

| Fichier             | Ce qui est testé |
|---------------------|------------------|
| `conftest.py`       | Fixture `client` partagée : client de test Flask en mode `TESTING`. |
| `test_operators.py` | `add`, `subtract`, `multiply`, `divide` de `operators.py` : résultats pour des entiers, décimaux et zéro, ordre des opérandes, division réelle (sans troncature) et `ZeroDivisionError`. |
| `test_calculate.py` | `calculate` de `app.py` : chaque opérateur, espaces, décimales, type du résultat, opérandes négatifs et en notation scientifique, nombre seul, rejet (`ValueError`) des expressions mal formées et des opérandes `inf`/`nan`, division par zéro (`ZeroDivisionError`) et dépassement de capacité (`OverflowError`). |
| `test_format.py`    | `format_result` de `app.py` : arrondi à 12 chiffres significatifs, suppression des zéros superflus, bascule en notation scientifique, absence de `-0`. |
| `test_routes.py`    | Route `/` : `GET` affiche un écran vide ; format du résultat affiché (`11` et non `11.0`, 12 chiffres significatifs, notation scientifique) ; tout résultat affiché est réutilisable comme opérande ; nombre seul et écran vide ; messages d'erreur en français ; une exception imprévue n'est pas masquée. |
| `test_interface.py` | `templates/index.html` rendu : chaque bouton de chiffre et d'opérateur affiche le caractère qu'il ajoute, seul `=` soumet le formulaire, `C` appelle `clearDisplay()`, titre et en-tête en français. |

### Hors couverture

Ces comportements sont vérifiés manuellement dans un navigateur ; la
procédure est décrite dans l'Issue correspondante.

- Le JavaScript (`appendToDisplay`, `clearDisplay`) n'est pas exécuté ; seule
  la structure HTML est vérifiée. En particulier, le comportement des boutons
  après un résultat ou une erreur n'est pas testé automatiquement. Le tester
  demanderait un navigateur automatisé (p. ex. Playwright ou Selenium).
- Le rendu visuel (`static/style.css`), comme les dimensions de l'écran
  d'affichage, n'est pas testé automatiquement.

## Ajouter un test

- Nommer le fichier `test_<module>.py` et chaque fonction `test_<comportement>`
  pour que pytest les découvre.
- Donner à chaque test un docstring qui énonce le comportement attendu.
- Utiliser la fixture `client` (sans import, fournie par `conftest.py`) pour
  envoyer des requêtes à l'application.
- Lorsqu'un nouveau test échoue à cause d'un bogue, ouvrir une Issue GitHub
  qui cite le test (voir la section « Flux de contribution » du
  [README principal](../README.md)).
