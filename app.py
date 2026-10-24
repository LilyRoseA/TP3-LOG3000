"""Point d'entrée de l'application web de calculatrice.

Définit l'application Flask et sa route unique ``/``, la fonction
``calculate``, qui analyse l'expression saisie avant de déléguer le calcul
aux fonctions du module ``operators``, et la fonction ``format_result``, qui
prépare le résultat pour l'écran de la calculatrice.
"""

import math
import re

from flask import Flask, request, render_template
from operators import add, subtract, multiply, divide

app = Flask(__name__)

# Associe les symboles saisis dans l'expression aux opérations correspondantes.
OPS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

# Un nombre : un signe « - » facultatif, puis une partie décimale et un exposant
# signé facultatifs. Couvre tout ce que l'écran affiche (« -1.5 », « 1e+16 »).
NUMBER = r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?"

# Un nombre, éventuellement suivi d'un opérateur de OPS et d'un second nombre.
# Comme le signe d'un opérande ou d'un exposant fait partie de NUMBER, il n'est
# jamais pris pour l'opérateur.
EXPRESSION_RE = re.compile(
    rf"({NUMBER})(?:([{re.escape(''.join(OPS))}])({NUMBER}))?"
)


def calculate(expr: str) -> float:
    """Évalue une expression contenant deux nombres et un opérateur, ou un nombre seul.

    Chaque nombre peut porter un signe ``-`` et être en notation scientifique,
    ce qui permet de réutiliser n'importe quel résultat affiché comme opérande.

    Args:
        expr: Expression textuelle, par exemple ``"2+3"``, ``"3--2"``,
            ``"1e+16*2"`` ou ``"42"``.

    Returns:
        Le résultat de l'opération sélectionnée, ou le nombre lui-même s'il
        n'y a pas d'opérateur (« = » appuyé sur un nombre).

    Raises:
        ValueError: Si l'expression est vide ou ne respecte pas la forme
            « nombre [opérateur nombre] ».
        OverflowError: Si un opérande ou le résultat dépasse la capacité
            d'un ``float``.
    """
    if not expr or not isinstance(expr, str):
        raise ValueError("expression vide")

    match = EXPRESSION_RE.fullmatch(expr.replace(" ", ""))
    if match is None:
        raise ValueError("expression mal formée")

    left, op_char, right = match.groups()
    if op_char is None:
        operands = (float(left),)
        result = operands[0]
    else:
        operands = (float(left), float(right))
        result = OPS[op_char](*operands)

    # float() et les opérations ne lèvent pas d'erreur en cas de dépassement :
    # ils produisent silencieusement inf. NUMBER exclut déjà « inf » et
    # « nan », donc une valeur non finie signifie forcément un dépassement.
    if not all(math.isfinite(x) for x in (*operands, result)):
        raise OverflowError("résultat trop grand")
    return result


def format_result(value: float) -> str:
    """Formate un résultat pour l'écran de la calculatrice.

    Args:
        value: Résultat numérique retourné par ``calculate``.

    Returns:
        Le nombre avec au plus 12 chiffres significatifs, sans zéros ni point
        décimal superflus (``11.0`` donne ``"11"``), en notation scientifique
        pour les très grands ou très petits nombres (``"1e+16"``).
    """
    # 12 chiffres masquent les erreurs d'arrondi binaires (0.1 + 0.2).
    # « + 0.0 » transforme -0.0 en 0.0 pour ne pas afficher « -0 ».
    return format(value + 0.0, ".12g")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Affiche la calculatrice et traite l'expression envoyée par le formulaire.

    Returns:
        Le gabarit HTML rendu avec le résultat ou un message d'erreur.
    """
    result = ""
    expression = request.form.get('display', '')
    # « = » sur un écran vide n'est pas une erreur : l'écran reste simplement vide.
    if request.method == 'POST' and expression.strip():
        # Les erreurs de saisie attendues sont affichées dans l'écran de la
        # calculatrice, avec un message fixe plutôt que le texte technique de
        # l'exception. Toute autre exception est un bogue : elle doit remonter.
        try:
            result = format_result(calculate(expression))
        except ValueError:
            result = "Erreur : expression invalide"
        except ZeroDivisionError:
            result = "Erreur : division par zéro"
        except OverflowError:
            result = "Erreur : résultat trop grand"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Mode debug (rechargement auto, traces détaillées) : développement local seulement.
    app.run(debug=True)