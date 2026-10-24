"""Opérations arithmétiques utilisées par la calculatrice."""


def add(a,b):
    """Additionne deux nombres.

    Args:
        a: Premier nombre.
        b: Deuxième nombre.

    Returns:
        La somme de ``a`` et ``b``.
    """
    return a + b


def subtract(a,b):
    """Soustrait ``a`` de ``b``.

    Args:
        a: Nombre soustrait.
        b: Nombre de départ.

    Returns:
        La différence ``b - a``.
    """
    return b - a


def multiply(a,b):
    """Élève ``a`` à la puissance ``b``.

    Args:
        a: Base.
        b: Exposant.

    Returns:
        La puissance ``a ** b``.
    """
    return a ** b


def divide(a,b):
    """Effectue une division entière de ``a`` par ``b``.

    Args:
        a: Dividende.
        b: Diviseur.

    Returns:
        Le quotient entier inférieur ou égal à la division de ``a`` par ``b``.

    Raises:
        ZeroDivisionError: Si ``b`` vaut zéro.
    """
    return a // b
