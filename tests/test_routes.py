"""Tests de la route ``/`` de ``app.py`` au moyen du client de test Flask.

Seule l'addition est utilisée pour les calculs valides : ces tests vérifient
le cheminement de la requête et l'affichage, pas l'arithmétique (voir
``test_operators.py``).
"""

import re

import pytest


def valeur_affichee(html):
    """Extrait la valeur du champ ``display`` de la page rendue.

    Args:
        html: Corps de la réponse, décodé en texte.

    Returns:
        Le contenu de l'attribut ``value`` du champ ``display``.
    """
    match = re.search(r'id="display" value="([^"]*)"', html)
    assert match, "champ display introuvable dans la page"
    return match.group(1)


def afficher(client, expression):
    """Soumet ``expression`` comme le ferait le bouton « = ».

    Args:
        client: Fixture ``client``.
        expression: Contenu du champ ``display`` envoyé.

    Returns:
        La valeur affichée dans la page renvoyée (code 200 vérifié).
    """
    reponse = client.post("/", data={"display": expression})
    assert reponse.status_code == 200
    return valeur_affichee(reponse.get_data(as_text=True))


def test_get_affiche_la_calculatrice_vide(client):
    """Un GET renvoie la page avec un écran vide."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)) == ""


def test_post_affiche_le_resultat(client):
    """Un POST valide affiche le résultat dans le champ ``display``."""
    assert afficher(client, "2+3") == "5"


@pytest.mark.parametrize("expression, affiche", [
    ("5+6", "11"),                  # pas de « .0 » superflu
    ("1.5+1", "2.5"),
    ("0.1+0.2", "0.3"),             # 12 chiffres significatifs au plus
    ("10000000000000000+1", "1e+16"),  # notation scientifique pour les grands nombres
    ("0.000000001+0", "1e-09"),        # et pour les très petits
])
def test_format_du_resultat(client, expression, affiche):
    """Le résultat est affiché sans décimales superflues ni artefacts d'arrondi."""
    assert afficher(client, expression) == affiche


@pytest.mark.parametrize("expression", ["11+0", "-1.5+0", "1e+16+0", "1e-09+0", "0.1+0.2"])
def test_resultat_affiche_reutilisable(client, expression):
    """Tout résultat affiché peut être renvoyé tel quel sans provoquer d'erreur.

    Simule « = » puis « + 0 = » : le second calcul doit redonner le premier
    résultat.
    """
    premier = afficher(client, expression)
    assert afficher(client, premier + "+0") == premier


def test_nombre_seul_affiche_le_nombre(client):
    """« = » sur un nombre seul affiche ce nombre plutôt qu'une erreur."""
    assert afficher(client, "2.5") == "2.5"


def test_ecran_vide_reste_vide(client):
    """« = » sur un écran vide ne produit pas d'erreur : l'écran reste vide."""
    assert afficher(client, "") == ""


def test_post_sans_champ_display_reste_vide(client):
    """Un formulaire sans champ ``display`` est traité comme un écran vide."""
    reponse = client.post("/", data={})
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)) == ""


def test_post_expression_invalide_affiche_une_erreur(client):
    """Une expression mal formée affiche un message d'erreur, pas une page 500."""
    assert afficher(client, "2+").startswith("Error:")


def test_post_division_par_zero_affiche_une_erreur(client):
    """La division par zéro est attrapée par la route et affichée comme erreur."""
    assert afficher(client, "5/0").startswith("Error:")


def test_depassement_affiche_un_message(client):
    """Un résultat trop grand affiche un message clair plutôt que « inf »."""
    assert afficher(client, "9" * 400 + "+1") == "Erreur : résultat trop grand"
