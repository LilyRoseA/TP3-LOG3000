"""Tests de ``app.calculate`` : analyse de l'expression et délégation du calcul.

Ces tests appellent la fonction directement, sans passer par Flask.
"""

import pytest

from app import calculate


@pytest.mark.parametrize("expression, attendu", [
    ("2+3", 5.0),
    ("8-3", 5.0),
    ("4*3", 12.0),
    ("7/2", 3.5),
])
def test_calculate_chaque_operateur(expression, attendu):
    """Chaque opérateur de ``OPS`` produit le résultat arithmétique attendu."""
    assert calculate(expression) == pytest.approx(attendu)


def test_calculate_ignore_les_espaces():
    """Les espaces autour des opérandes et de l'opérateur sont ignorés."""
    assert calculate(" 12 + 7 ") == 19.0


def test_calculate_accepte_les_decimales():
    """Les opérandes sont convertis en ``float`` ; les décimales sont acceptées."""
    assert calculate("1.5+2.25") == pytest.approx(3.75)


def test_calculate_retourne_un_float():
    """Le résultat est un ``float``, même pour des opérandes entiers."""
    assert isinstance(calculate("2+3"), float)


@pytest.mark.parametrize("expression", [
    "",        # expression vide
    "42",      # aucun opérateur
    "+3",      # opérande gauche manquant
    "3+",      # opérande droit manquant
    "-3+2",    # le signe négatif compte comme un second opérateur
    "1+2+3",   # plusieurs opérateurs
    "a+2",     # opérande non numérique
    "2+b",
])
def test_calculate_rejette_les_expressions_invalides(expression):
    """Toute expression mal formée lève ``ValueError``."""
    with pytest.raises(ValueError):
        calculate(expression)


def test_calculate_rejette_un_type_non_textuel():
    """Une valeur absente (``None``) est traitée comme une expression vide."""
    with pytest.raises(ValueError):
        calculate(None)


def test_calculate_division_par_zero():
    """La division par zéro n'est pas une erreur de format : ``ZeroDivisionError``."""
    with pytest.raises(ZeroDivisionError):
        calculate("5/0")
