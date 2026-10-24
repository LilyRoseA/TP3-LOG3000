# Calculatrice Web avec Flask

**Numéro d’équipe :** 4 (Lily-Rose Arès - 2377089 et Thierry Poulin - 2330561)

## Description

Application web de calculatrice simple, développée en Python avec Flask.
L'utilisateur compose une expression à l'aide des boutons de l'interface ;
l'expression est envoyée au serveur, qui la calcule et renvoie la page avec
le résultat affiché à l'écran de la calculatrice.

### Portée

- Une seule opération binaire par expression : addition (`+`),
  soustraction (`-`), multiplication (`*`) et division (`/`). Un nombre
  seul est aussi accepté (« = » l'affiche tel quel).
- Les opérandes sont des nombres réels ; chacun peut porter un signe `-`
  (p. ex. `3--2`) ou être en notation scientifique (p. ex. `1e+16`).
- Les résultats sont affichés sans décimales superflues, avec au plus
  12 chiffres significatifs (`5+6` donne `11`, `7/2` donne `3.5`), et en
  notation scientifique pour les très grands ou très petits nombres. Tout
  résultat affiché peut servir d'opérande au calcul suivant.
- Hors portée : parenthèses, priorité des opérations, expressions à
  plusieurs opérateurs et saisie au clavier. L'interface n'a pas de bouton de
  point décimal : un nombre décimal ne peut être saisi qu'en réutilisant un
  résultat (p. ex. `7/2` donne `3.5`, puis `*`, `2`).
- Les erreurs affichent un court message en français au lieu d'un résultat :
  `Erreur : expression invalide`, `Erreur : division par zéro` ou
  `Erreur : résultat trop grand`.

> Ce comportement est vérifié par la suite de tests (voir [Tests](#tests)).
> Les bogues trouvés dans la base de code initiale et leurs correctifs sont
> documentés dans les [Issues fermées](https://github.com/LilyRoseA/TP3-LOG3000/issues?q=is%3Aissue+is%3Aclosed)
> et les [Pull Requests](https://github.com/LilyRoseA/TP3-LOG3000/pulls?q=is%3Apr+is%3Aclosed)
> correspondantes.

## Structure du projet

```
.
├── app.py             # Serveur Flask : route « / » et analyse de l'expression (calculate)
├── operators.py       # Fonctions arithmétiques add, subtract, multiply, divide
├── requirements.txt   # Dépendances Python (Flask, pytest)
├── pytest.ini         # Configuration de pytest
├── templates/         # Gabarits HTML (Jinja2)  → voir templates/README.md
│   └── index.html
├── static/            # Fichiers servis tels quels (CSS)  → voir static/README.md
│   └── style.css
├── tests/             # Tests automatisés (pytest)  → voir tests/README.md
└── docs/              # Captures d'écran des correctifs visuels  → voir docs/README.md
```

Chaque répertoire contient son propre `README.md` décrivant son rôle, ses
fichiers et ses dépendances.

**Flux d'une requête :** `index.html` (bouton `=`) → `POST /` → `app.index()`
→ `app.calculate()` → fonction de `operators.py` → `index.html` rendu avec le
résultat.

## Prérequis

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/) 3.9 ou plus récent
- `pip`, le gestionnaire de paquets de Python (inclus avec Python)

Vérifier l'installation :

```bash
git --version
python --version
python -m pip --version
```

> Selon le système, la commande peut être `python3` au lieu de `python`.

## Installation

1. Cloner le dépôt et s'y déplacer :

   ```bash
   git clone https://github.com/LilyRoseA/TP3-LOG3000.git
   cd TP3-LOG3000
   ```

2. Créer un environnement virtuel (recommandé, ignoré par Git) :

   ```bash
   python -m venv .venv
   ```

3. Activer l'environnement virtuel :

   | Système                  | Commande                       |
   |--------------------------|--------------------------------|
   | Windows (PowerShell)     | `.venv\Scripts\Activate.ps1`   |
   | Windows (cmd)            | `.venv\Scripts\activate.bat`   |
   | macOS / Linux / Git Bash | `source .venv/bin/activate`    |

   > Sous PowerShell, si l'exécution de scripts est bloquée :
   > `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

4. Installer les dépendances :

   ```bash
   python -m pip install -r requirements.txt
   ```

## Utilisation

### Lancer l'application

Depuis la racine du projet, avec l'environnement virtuel activé :

| Mode | Commande | Usage |
|------|----------|-------|
| Normal | `flask --app app run` | Utilisation courante, démonstration. |
| Développement | `flask --app app run --debug` | Rechargement automatique à chaque modification du code et traces d'erreur détaillées dans le navigateur. |
| Développement (raccourci) | `python app.py` | Équivaut au mode développement : `app.py` active toujours le mode debug. |

Ouvrir ensuite <http://127.0.0.1:5000> dans un navigateur. Arrêter le serveur
avec `Ctrl+C`. Les options `--host` et `--port` changent l'adresse d'écoute
(p. ex. `flask --app app run --port 8000`).

> Le mode debug permet d'exécuter du code Python depuis le navigateur en cas
> d'erreur : ne jamais l'activer sur un serveur accessible par d'autres
> machines. Le serveur intégré de Flask, même sans debug, est conçu pour le
> développement ; un déploiement réel passerait par un serveur WSGI comme
> [Waitress](https://docs.pylonsproject.org/projects/waitress/) ou
> [Gunicorn](https://gunicorn.org/).

Chaque requête est journalisée dans le terminal au format habituel de
Werkzeug, p. ex. `"GET /static/style.css HTTP/1.1" 304 -` : le code `304`
signifie que le navigateur réutilise sa copie en cache de la feuille de
style, et `-` indique qu'aucun corps de réponse n'a été envoyé. Une ligne
`"GET /favicon.ico HTTP/1.1" 404 -` est aussi normale : le navigateur demande
une icône d'onglet que le projet ne fournit pas.

### Utiliser la calculatrice

1. Composer l'expression avec les boutons : un nombre, un opérateur, puis un
   second nombre (p. ex. `12`, `+`, `7`). Pour un nombre négatif, appuyer sur
   `-` juste avant ses chiffres (p. ex. `3`, `*`, `-`, `2`). Le champ
   d'affichage est en lecture seule ; le clavier n'est pas utilisé.
2. Appuyer sur `=` pour envoyer l'expression au serveur. Le résultat (ou un
   message d'erreur) remplace l'expression à l'écran.
3. Appuyer sur `C` pour effacer l'écran et recommencer.

Après un résultat, un opérateur poursuit le calcul à partir de ce résultat
(p. ex. après `5`, appuyer sur `*`, `2`, puis `=` donne `10`), alors qu'un
chiffre commence une nouvelle saisie. Après une erreur, n'importe quel bouton
efface d'abord le message.

## Tests

Les tests unitaires utilisent [pytest](https://docs.pytest.org/) (installé
par `requirements.txt`) et se trouvent dans le répertoire `tests/`.

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
python -m pytest            # exécuter toute la suite
python -m pytest -v         # afficher le détail de chaque test
python -m pytest tests/test_operators.py   # exécuter un seul fichier
```

Aucun serveur n'a besoin d'être lancé. Le contenu et la couverture des tests
sont décrits dans [`tests/README.md`](tests/README.md).

## Flux de contribution

Le travail est organisé autour des Issues, des branches et des Pull Requests
GitHub. La branche `main` doit toujours contenir du code fonctionnel dont les
tests passent ; on n'y pousse pas directement.

1. **Issue** — Tout bogue ou toute tâche commence par une
   [Issue](https://github.com/LilyRoseA/TP3-LOG3000/issues) qui décrit le
   problème, les étapes de reproduction (ou le test qui échoue) et le
   résultat attendu. L'Issue est assignée à un membre de l'équipe.
2. **Branche** — Créer une branche à partir de `main` à jour, une par Issue,
   nommée `<type>/<numéro>-<description-courte>` :

   ```bash
   git switch main
   git pull
   git switch -c fix/12-description-courte
   ```

   Types usuels : `fix` (correction de bogue), `feat` (fonctionnalité),
   `docs` (documentation), `test` (tests).

   Si le correctif dépend d'un autre qui n'est pas encore fusionné, créer la
   branche à partir de la branche dont il dépend, et l'indiquer dans la PR
   pour qu'elle soit fusionnée après.
3. **Commits** — Des commits petits et ciblés, suivant les
   [Conventional Commits](https://www.conventionalcommits.org/fr/) :
   `fix(app): rejette les expressions sans opérande droit`. Le message
   explique comment la modification règle le problème.
4. **Tests** — Avant d'ouvrir la PR, exécuter `python -m pytest` et
   s'assurer que le test qui échouait passe désormais, sans régression.
5. **Pull Request** — Pousser la branche (`git push -u origin <branche>`) et
   ouvrir une PR vers `main`. La description résume le correctif, indique
   les tests exécutés et référence l'Issue avec `Closes #<numéro>` pour la
   fermer automatiquement à la fusion.
6. **Conflits** — Si la PR entre en conflit avec `main`, fusionner `main` à
   jour dans la branche, résoudre en conservant le comportement des deux
   côtés, réexécuter toute la suite de tests, puis pousser la branche :

   ```bash
   git switch <branche>
   git merge origin/main
   # résoudre, puis :
   python -m pytest
   git commit
   git push
   ```

7. **Revue et fusion** — Un autre membre de l'équipe relit la PR et laisse
   une revue (changement, résultat des tests, conflits résolus), puis la
   fusionne avec un commit de fusion (« Create a merge commit »), qui garde
   l'historique de la branche. La branche est ensuite supprimée et la suite de
   tests complète est réexécutée sur `main`.
