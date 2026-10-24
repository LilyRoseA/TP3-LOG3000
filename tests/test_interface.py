"""Tests de l'interface ``templates/index.html`` telle que rendue par Flask.

Le JavaScript n'est pas exécuté : on vérifie la structure HTML, en particulier
que chaque bouton affiche le caractère qu'il ajoute à l'expression.
"""

import re
from html.parser import HTMLParser

import pytest

# Capture le caractère passé à appendToDisplay('x') dans l'attribut onclick.
APPEND_RE = re.compile(r"appendToDisplay\('(.)'\)")


class LecteurDeBoutons(HTMLParser):
    """Collecte les boutons de la page avec leur étiquette et leur action.

    Attributes:
        boutons: Liste de dictionnaires ``{"etiquette", "onclick", "type"}``,
            dans l'ordre d'apparition.
    """

    def __init__(self):
        super().__init__()
        self.boutons = []
        self._courant = None

    def handle_starttag(self, tag, attrs):
        """Ouvre un nouveau bouton lorsqu'une balise ``<button>`` commence."""
        if tag == "button":
            attrs = dict(attrs)
            self._courant = {
                "etiquette": "",
                "onclick": attrs.get("onclick", ""),
                "type": attrs.get("type", ""),
            }

    def handle_data(self, data):
        """Accumule le texte affiché à l'intérieur du bouton courant."""
        if self._courant is not None:
            self._courant["etiquette"] += data

    def handle_endtag(self, tag):
        """Termine le bouton courant à la fermeture de ``</button>``."""
        if tag == "button" and self._courant is not None:
            self._courant["etiquette"] = self._courant["etiquette"].strip()
            self.boutons.append(self._courant)
            self._courant = None


@pytest.fixture
def boutons(client):
    """Boutons de la page d'accueil rendue.

    Returns:
        La liste produite par ``LecteurDeBoutons``.
    """
    lecteur = LecteurDeBoutons()
    lecteur.feed(client.get("/").get_data(as_text=True))
    return lecteur.boutons


def bouton_qui_ajoute(boutons, caractere):
    """Retourne le bouton dont le ``onclick`` ajoute ``caractere`` à l'affichage.

    Args:
        boutons: Liste produite par ``LecteurDeBoutons``.
        caractere: Caractère passé à ``appendToDisplay``.

    Returns:
        Le dictionnaire du bouton correspondant.
    """
    for bouton in boutons:
        match = APPEND_RE.search(bouton["onclick"])
        if match and match.group(1) == caractere:
            return bouton
    pytest.fail(f"aucun bouton n'ajoute {caractere!r}")


@pytest.mark.parametrize("caractere", list("0123456789"))
def test_etiquette_des_chiffres(boutons, caractere):
    """Chaque bouton de chiffre affiche exactement le chiffre qu'il ajoute."""
    assert bouton_qui_ajoute(boutons, caractere)["etiquette"] == caractere


@pytest.mark.parametrize("caractere", ["+", "-", "*", "/"])
def test_etiquette_des_operateurs(boutons, caractere):
    """Chaque bouton d'opérateur affiche le symbole qu'il ajoute."""
    assert bouton_qui_ajoute(boutons, caractere)["etiquette"] == caractere


def test_seul_le_bouton_egal_soumet_le_formulaire(boutons):
    """Seul « = » est de type ``submit`` ; les autres ne doivent pas envoyer le formulaire."""
    soumission = [b["etiquette"] for b in boutons if b["type"] == "submit"]
    assert soumission == ["="]


def test_bouton_effacer(boutons):
    """Le bouton « C » appelle ``clearDisplay()``."""
    effacer = [b for b in boutons if b["etiquette"] == "C"]
    assert len(effacer) == 1
    assert "clearDisplay()" in effacer[0]["onclick"]
