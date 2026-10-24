# `static/` — Ressources statiques

## Raison d'être

Ce répertoire contient les fichiers servis tels quels au navigateur (CSS,
et éventuellement images ou JavaScript). Flask les expose par défaut sous
l'URL `/static/` : ce nom de dossier ne doit pas changer.

## Fichiers

| Fichier     | Responsabilité |
|-------------|----------------|
| `style.css` | Apparence de la calculatrice : centrage de la page, écran d'affichage, grille de boutons 4 colonnes et couleurs des opérateurs. |

## Dépendances et hypothèses

- `style.css` cible les éléments de [`templates/index.html`](../templates/README.md) :
  la classe `.calculator`, l'identifiant `#display`, et les classes `.buttons`,
  `.btn` et `.operator`. Renommer l'un d'eux dans le HTML exige la même
  modification ici.
- La grille `.buttons` suppose quatre boutons par rangée ; l'ordre des
  boutons dans le HTML détermine donc leur position.
- Aucun préprocesseur ni outil de compilation : le CSS est servi directement.
