# Calculatrice Web avec Flask

**Numéro d’équipe :** 4 (Lily-Rose Arès - 2377089 et Thierry Poulin - 2330561)

## Description

Application web de calculatrice simple, développée en Python avec Flask.
L'utilisateur compose une expression à l'aide des boutons de l'interface ;
l'expression est envoyée au serveur, qui la calcule et renvoie la page avec
le résultat affiché à l'écran de la calculatrice.

### Portée

- Une seule opération binaire par expression : addition (`+`),
  soustraction (`-`), multiplication (`*`) et division (`/`).
- Les opérandes sont des nombres positifs ; les résultats sont des nombres
  à virgule flottante (p. ex. `2+3` donne `5.0`).
- Hors portée : parenthèses, priorité des opérations, expressions à
  plusieurs opérateurs et nombres négatifs (un `-` en tête est interprété
  comme un opérateur).
- Les expressions invalides (vide, sans opérateur, opérande manquant ou non
  numérique) affichent un message `Error: ...` au lieu d'un résultat.

## Structure du projet

```
.
├── app.py             # Serveur Flask : route « / » et analyse de l'expression (calculate)
├── operators.py       # Fonctions arithmétiques add, subtract, multiply, divide
├── requirements.txt   # Dépendances Python (Flask, pytest)
├── templates/         # Gabarits HTML (Jinja2)  → voir templates/README.md
│   └── index.html
└── static/            # Fichiers servis tels quels (CSS)  → voir static/README.md
    └── style.css
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

```bash
python app.py
```

Le serveur démarre en mode debug (rechargement automatique à chaque
modification du code). Ouvrir ensuite <http://127.0.0.1:5000> dans un
navigateur. Arrêter le serveur avec `Ctrl+C`.

> Le mode debug est destiné au développement local seulement ; ne pas
> l'utiliser pour un déploiement.

### Utiliser la calculatrice

1. Composer l'expression avec les boutons : un nombre, un opérateur, puis un
   second nombre (p. ex. `12`, `+`, `7`). Le champ d'affichage est en lecture
   seule ; le clavier n'est pas utilisé.
2. Appuyer sur `=` pour envoyer l'expression au serveur. Le résultat (ou un
   message d'erreur) remplace l'expression à l'écran.
3. Appuyer sur `C` pour effacer l'écran et recommencer.

Il est possible de poursuivre un calcul à partir du résultat affiché (p. ex.
après `5.0`, appuyer sur `*`, `2`, puis `=`).

## Tests

Les tests unitaires utilisent [pytest](https://docs.pytest.org/) (installé
par `requirements.txt`) et se trouvent dans le répertoire `tests/`.

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
python -m pytest            # exécuter toute la suite
python -m pytest -v         # afficher le détail de chaque test
python -m pytest tests/<fichier>.py   # exécuter un seul fichier
```

> Utiliser `python -m pytest` (plutôt que `pytest`) ajoute la racine du
> projet au chemin d'import, ce qui permet aux tests d'importer `app` et
> `operators`.

Le contenu et la couverture des tests sont décrits dans `tests/README.md`.

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
6. **Revue et fusion** — Un autre membre de l'équipe relit la PR, puis la
   fusionne. La branche est ensuite supprimée et la suite de tests complète
   est réexécutée sur `main`.
