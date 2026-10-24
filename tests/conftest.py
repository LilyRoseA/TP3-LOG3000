"""Fixtures partagées par les tests."""

import pytest

from app import app


@pytest.fixture
def client():
    """Client de test Flask : envoie des requêtes sans démarrer de serveur.

    Returns:
        Un ``FlaskClient`` lié à l'application en mode test (les exceptions
        non attrapées remontent dans le test au lieu de produire une page 500).
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
