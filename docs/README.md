# `docs/` — Documentation complémentaire

## Raison d'être

Ce répertoire contient les pièces de documentation qui ne sont pas du code :
principalement les captures d'écran qui prouvent qu'un correctif visuel
fonctionne, puisque le rendu CSS n'est pas couvert par la suite de tests
automatisée (voir [`tests/README.md`](../tests/README.md)).

## Fichiers

| Fichier | Contenu |
|---------|---------|
| `issue-6-avant-800.png` | Issue #6, avant le correctif, fenêtre de 800 px : l'écran d'affichage dépasse à droite de la grille de boutons. |
| `issue-6-apres-800.png` | Issue #6, après le correctif, fenêtre de 800 px : l'écran est aligné sur la grille ; le reste est inchangé. |
| `issue-6-avant-360.png` | Issue #6, avant le correctif, cadre de 360 px (fond rouge autour du cadre) : la calculatrice déborde des deux côtés. |
| `issue-6-apres-360.png` | Issue #6, après le correctif, cadre de 360 px : la calculatrice tient dans le cadre. |

## Conventions et hypothèses

- Nommer chaque capture `issue-<numéro>-<avant|apres>-<largeur>.png` et la
  décrire dans le tableau ci-dessus.
- Les captures sont faites avec Chrome sans interface, l'application étant
  lancée avec `flask --app app run`, par exemple :

  ```bash
  chrome --headless=new --window-size=800,800 --screenshot=capture.png http://127.0.0.1:5000/
  ```

  Chrome sans interface impose une largeur de fenêtre minimale d'environ
  500 px ; pour une largeur inférieure, charger l'application dans un
  `<iframe>` de la largeur voulue.
- Les captures reflètent l'état de la branche du correctif : d'autres bogues
  corrigés sur d'autres branches (p. ex. les étiquettes « 02 » et « 88 »,
  issue #4) peuvent encore y apparaître.
