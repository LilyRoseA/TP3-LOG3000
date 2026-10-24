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


@pytest.mark.parametrize("expression, attendu", [
    ("-2+1", -1.0),
    ("-2.5+0.5", -2.0),
    ("3+-2", 1.0),
    ("-3+-2", -5.0),
    ("1e+16+1", 1e16 + 1),
    ("1e-9+1", 1.000000001),
    ("-1e+16+1", -1e16 + 1),
    ("1+1e-9", 1.000000001),
])
def test_calculate_accepte_les_operandes_signes_et_scientifiques(expression, attendu):
    """Chaque opérande peut être négatif ou en notation scientifique.

    Un « - » en tête d'opérande est un signe, et le signe d'un exposant
    (``e+16``, ``e-9``) fait partie du nombre : ni l'un ni l'autre n'est
    l'opérateur de l'expression. Un résultat affiché peut donc toujours être
    réutilisé comme opérande.
    """
    assert calculate(expression) == pytest.approx(attendu)


@pytest.mark.parametrize("expression, attendu", [
    ("42", 42.0),
    ("-7", -7.0),
    ("2.5", 2.5),
    ("1e+16", 1e16),
])
def test_calculate_nombre_seul(expression, attendu):
    """Un nombre seul, sans opérateur, est retourné tel quel (« = » sur un nombre)."""
    assert calculate(expression) == attendu


@pytest.mark.parametrize("expression", [
    "",        # expression vide
    "+3",      # seul « - » est accepté comme signe
    "3+",      # opérande droit manquant
    "--3+2",   # deux signes sur un même opérande
    "3+--2",
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


@pytest.mark.parametrize("expression", ["inf+1", "1+inf", "nan+1", "-inf"])
def test_calculate_rejette_les_operandes_non_finis(expression):
    """« inf » et « nan » ne sont pas des nombres saisissables : ``ValueError``."""
    with pytest.raises(ValueError):
        calculate(expression)


@pytest.mark.parametrize("expression", [
    "9" * 400 + "+1",   # opérande trop grand pour un float
    "9" * 400,          # nombre seul trop grand
    "1e200*1e200",      # résultat trop grand pour un float
])
def test_calculate_depassement(expression):
    """Un opérande ou un résultat qui dépasse la capacité d'un float lève ``OverflowError``.

    Sans cette vérification, le calcul produit silencieusement ``inf``.
    """
    with pytest.raises(OverflowError):
        calculate(expression)
