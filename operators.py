"""Opérations arithmétiques utilisées par la calculatrice.

Chaque fonction reçoit deux opérandes numériques (des ``float`` produits par
``app.calculate``) et retourne le résultat de l'opération correspondante.
"""


def add(a,b):
    """Additionne deux nombres.

    Args:
        a: Premier nombre.
        b: Deuxième nombre.

    Returns:
        La somme ``a + b``.
    """
    return a + b


def subtract(a,b):
    """Soustrait ``b`` de ``a``.

    Args:
        a: Nombre de départ (opérande de gauche).
        b: Nombre soustrait (opérande de droite).

    Returns:
        La différence ``a - b``.
    """
    return b - a


def multiply(a,b):
    """Multiplie deux nombres.

    Args:
        a: Premier facteur.
        b: Deuxième facteur.

    Returns:
        Le produit ``a * b``.
    """
    return a * b


def divide(a,b):
    """Divise ``a`` par ``b``.

    Args:
        a: Dividende (opérande de gauche).
        b: Diviseur (opérande de droite).

    Returns:
        Le quotient réel ``a / b``.

    Raises:
        ZeroDivisionError: Si ``b`` vaut zéro.
    """
    return a // b
