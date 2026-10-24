"""Tests unitaires de ``app.format_result`` : affichage d'un résultat numérique."""

import pytest

from app import format_result


@pytest.mark.parametrize("valeur, affiche", [
    (11.0, "11"),
    (-1.5, "-1.5"),
    (1 / 3, "0.333333333333"),                 # 12 chiffres significatifs
    (123456789012.0, "123456789012"),          # 12 chiffres : pas de notation scientifique
    (1234567890123.0, "1.23456789012e+12"),    # au-delà : notation scientifique
    (1e-9, "1e-09"),
    (-0.0, "0"),                               # pas de « -0 »
])
def test_format_result(valeur, affiche):
    """Le résultat est arrondi à 12 chiffres significatifs, sans zéros superflus."""
    assert format_result(valeur) == affiche
