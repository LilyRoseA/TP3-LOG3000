"""Point d'entrée de l'application web de calculatrice.

Définit l'application Flask, la route unique ``/`` et la fonction
``calculate`` qui analyse l'expression saisie avant de déléguer le calcul
aux fonctions du module ``operators``.
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

# Deux nombres séparés par un opérateur de OPS. Comme le signe d'un opérande ou
# d'un exposant fait partie de NUMBER, il n'est jamais pris pour l'opérateur.
EXPRESSION_RE = re.compile(
    rf"({NUMBER})([{re.escape(''.join(OPS))}])({NUMBER})"
)


def calculate(expr: str):
    """Évalue une expression contenant deux nombres et un opérateur.

    Chaque nombre peut porter un signe ``-`` et être en notation scientifique,
    ce qui permet de réutiliser n'importe quel résultat affiché comme opérande.

    Args:
        expr: Expression textuelle, par exemple ``"2+3"``, ``"3--2"`` ou
            ``"1e+16*2"``.

    Returns:
        Le résultat de l'opération sélectionnée.

    Raises:
        ValueError: Si l'expression est vide ou ne respecte pas la forme
            « nombre opérateur nombre ».
        OverflowError: Si un opérande ou le résultat dépasse la capacité
            d'un ``float``.
    """
    if not expr or not isinstance(expr, str):
        raise ValueError("empty expression")

    match = EXPRESSION_RE.fullmatch(expr.replace(" ", ""))
    if match is None:
        raise ValueError("invalid expression format")

    left, op_char, right = match.groups()
    a, b = float(left), float(right)
    result = OPS[op_char](a, b)

    # float() et les opérations ne lèvent pas d'erreur en cas de dépassement :
    # ils produisent silencieusement inf. NUMBER exclut déjà « inf » et
    # « nan », donc une valeur non finie signifie forcément un dépassement.
    if not all(math.isfinite(x) for x in (a, b, result)):
        raise OverflowError("result too large")
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    """Affiche la calculatrice et traite l'expression envoyée par le formulaire.

    Returns:
        Le gabarit HTML rendu avec le résultat ou un message d'erreur.
    """
    result = ""
    if request.method == 'POST':
        expression = request.form.get('display', '')
        try:
            result = calculate(expression)
        except OverflowError:
            result = "Erreur : résultat trop grand"
        except Exception as e:
            # L'erreur est affichée dans l'écran de la calculatrice plutôt
            # que de renvoyer une page d'erreur HTTP à l'utilisateur.
            result = f"Error: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Mode debug (rechargement auto, traces détaillées) : développement local seulement.
    app.run(debug=True)