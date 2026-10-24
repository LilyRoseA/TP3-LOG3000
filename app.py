"""Point d'entrée de l'application web de calculatrice.

Définit l'application Flask, la route unique ``/`` et la fonction
``calculate`` qui analyse l'expression saisie avant de déléguer le calcul
aux fonctions du module ``operators``.
"""

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


def calculate(expr: str):
    """Évalue une expression contenant deux nombres et un opérateur.

    Args:
        expr: Expression textuelle, par exemple ``"2+3"``.

    Returns:
        Le résultat de l'opération sélectionnée.

    Raises:
        ValueError: Si l'expression est vide, mal formée ou contient des
            opérandes qui ne sont pas numériques.
    """
    if not expr or not isinstance(expr, str):
        raise ValueError("empty expression")

    s = expr.replace(" ", "")

    op_pos = -1
    op_char = None

    # Un seul opérateur est accepté. Un signe « - » devant un nombre compte
    # aussi comme opérateur : les opérandes négatifs ne sont donc pas gérés.
    for i, ch in enumerate(s):
        if ch in OPS:
            if op_pos != -1:
                raise ValueError("only one operator is allowed")
            op_pos = i
            op_char = ch

    if op_pos <= 0 or op_pos >= len(s) - 1:
        # Aucun opérateur trouvé (op_pos == -1), ou opérateur sans opérande
        # d'un côté (au début ou à la fin de l'expression).
        raise ValueError("invalid expression format")

    left = s[:op_pos]
    right = s[op_pos+1:]

    try:
        a = float(left)
        b = float(right)
    except ValueError:
        raise ValueError("operands must be numbers")

    return OPS[op_char](a, b)

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
        except Exception as e:
            # L'erreur est affichée dans l'écran de la calculatrice plutôt
            # que de renvoyer une page d'erreur HTTP à l'utilisateur.
            result = f"Error: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Mode debug (rechargement auto, traces détaillées) : développement local seulement.
    app.run(debug=True)