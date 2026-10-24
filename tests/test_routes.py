"""Tests de la route ``/`` de ``app.py`` au moyen du client de test Flask.

Seule l'addition est utilisée pour les calculs valides : ces tests vérifient
le cheminement de la requête, pas l'arithmétique (voir ``test_operators.py``).
"""

import re


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


def test_get_affiche_la_calculatrice_vide(client):
    """Un GET renvoie la page avec un écran vide."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)) == ""


def test_post_affiche_le_resultat(client):
    """Un POST valide affiche le résultat dans le champ ``display``."""
    reponse = client.post("/", data={"display": "2+3"})
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)) == "5.0"


def test_post_expression_invalide_affiche_une_erreur(client):
    """Une expression mal formée affiche un message d'erreur, pas une page 500."""
    reponse = client.post("/", data={"display": "2+"})
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)).startswith("Error:")


def test_post_division_par_zero_affiche_une_erreur(client):
    """La division par zéro est attrapée par la route et affichée comme erreur."""
    reponse = client.post("/", data={"display": "5/0"})
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)).startswith("Error:")


def test_post_sans_champ_display_affiche_une_erreur(client):
    """Un formulaire sans champ ``display`` est traité comme une expression vide."""
    reponse = client.post("/", data={})
    assert reponse.status_code == 200
    assert valeur_affichee(reponse.get_data(as_text=True)).startswith("Error:")
