# `templates/` — Interface utilisateur

## Raison d'être

Ce répertoire contient les gabarits HTML rendus par Flask. Flask cherche les
gabarits dans `templates/` par défaut : ce nom de dossier ne doit pas changer.

## Fichiers

| Fichier      | Responsabilité |
|--------------|----------------|
| `index.html` | Page unique de la calculatrice : écran d'affichage, grille de boutons et petit script JavaScript qui construit l'expression côté client. |

## Fonctionnement

1. Les boutons de chiffres et d'opérateurs appellent `appendToDisplay()`, qui
   ajoute un caractère dans le champ `display`. Le bouton `C` appelle
   `clearDisplay()`. Juste après une réponse du serveur (variable
   `reponseAffichee`, initialisée par Jinja à partir de `result`), un chiffre
   commence une nouvelle saisie, un opérateur poursuit le calcul à partir du
   résultat, et un message d'erreur est effacé avant tout ajout.
2. Le bouton `=` soumet le formulaire en `POST` vers `/`.
3. `app.py` lit le champ `display`, calcule le résultat et rend de nouveau
   `index.html` avec la variable `result`, affichée dans le champ `display`.

## Dépendances et hypothèses

- Rendu par Jinja2 (inclus avec Flask) via `render_template('index.html', result=...)`
  dans `app.py`. La variable `result` doit toujours être fournie (chaîne vide
  au premier affichage).
- Le nom du champ `display` est le contrat avec le backend : le renommer
  exige de modifier `request.form.get('display')` dans `app.py`.
- La feuille de style est chargée par `url_for('static', filename='style.css')`,
  voir [`static/`](../static/README.md).
- Les caractères envoyés par les boutons (`+`, `-`, `*`, `/`) doivent
  correspondre aux clés du dictionnaire `OPS` de `app.py`.
- Aucune bibliothèque JavaScript externe n'est utilisée.
