"""Tests unitaires des fonctions arithmétiques de ``operators.py``.

Les valeurs attendues suivent le comportement documenté dans les docstrings
(opérande de gauche ``a``, opérande de droite ``b``). Les cas sont choisis
pour que l'ordre des opérandes compte (p. ex. ``5 - 3`` et non ``3 - 3``).
"""

import pytest

from operators import add, subtract, multiply, divide


@pytest.mark.parametrize("a, b, attendu", [
    (2, 3, 5),
    (2.5, 0.5, 3.0),
    (0, 7, 7),
])
def test_add(a, b, attendu):
    """``add(a, b)`` retourne la somme ``a + b``."""
    assert add(a, b) == attendu


@pytest.mark.parametrize("a, b, attendu", [
    (5, 3, 2),
    (3, 5, -2),
    (10, 0, 10),
])
def test_subtract(a, b, attendu):
    """``subtract(a, b)`` retourne ``a - b`` (et non ``b - a``)."""
    assert subtract(a, b) == attendu


@pytest.mark.parametrize("a, b, attendu", [
    (2, 3, 6),
    (4, 2.5, 10.0),
    (7, 0, 0),
])
def test_multiply(a, b, attendu):
    """``multiply(a, b)`` retourne le produit ``a * b``."""
    assert multiply(a, b) == attendu


@pytest.mark.parametrize("a, b, attendu", [
    (7, 2, 3.5),
    (1, 4, 0.25),
    (-7, 2, -3.5),
])
def test_divide(a, b, attendu):
    """``divide(a, b)`` retourne le quotient réel, sans troncature."""
    assert divide(a, b) == pytest.approx(attendu)


def test_divide_par_zero():
    """Diviser par zéro lève ``ZeroDivisionError`` (attrapée plus haut par la route)."""
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
