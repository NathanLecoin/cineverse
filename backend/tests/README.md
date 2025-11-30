# Tests CineVerse Backend

## 📋 Vue d'ensemble

**20 tests essentiels** couvrant les fonctionnalités critiques du backend :
- **10 tests unitaires** : Fonctions isolées (CRUD, sécurité)
- **10 tests d'intégration** : Workflows API complets

## 📊 Statistiques

- ✅ **20/20 tests passent** (100% de réussite)
- ⚡ **~7 secondes** d'exécution totale
- 🎯 **Couvre 100%** des fonctionnalités essentielles

## 🗂️ Organisation

```
tests/
├── conftest.py              # Fixtures partagées (db, client, users, tokens)
├── test_integration.py      # 10 tests d'intégration API
└── unit/
    ├── conftest.py          # Configuration tests unitaires
    └── test_unit.py         # 10 tests unitaires
```

## 🎯 Tests Unitaires (10)

**Fichier** : `tests/unit/test_unit.py`

1. **test_password_hashing_and_verification** - Hash et vérification de mot de passe
2. **test_jwt_token_creation_and_decoding** - Création et décodage JWT
3. **test_create_user_with_password_hash** - Création utilisateur avec hash
4. **test_authenticate_user_success_and_failure** - Authentification (succès/échec)
5. **test_create_and_get_movie** - CRUD film
6. **test_create_review_for_movie** - Création de review
7. **test_add_movie_to_watchlist** - Ajout à la watchlist
8. **test_check_movie_in_watchlist** - Vérification présence dans watchlist
9. **test_watchlist_prevents_duplicates** - Gestion des doublons
10. **test_password_hash_uses_salt** - Unicité des hashs (salt)

## 🌐 Tests d'Intégration (10)

**Fichier** : `tests/test_integration.py`

1. **test_user_registration** - Inscription d'un utilisateur
2. **test_user_login** - Connexion et obtention du token JWT
3. **test_get_current_user_with_token** - Récupération du profil avec token
4. **test_list_movies_public** - Liste des films (accès public)
5. **test_create_movie_requires_admin** - Création de film (admin uniquement)
6. **test_create_review_workflow** - Workflow complet de création de review
7. **test_add_movie_to_watchlist_workflow** - Workflow ajout à la watchlist
8. **test_get_user_watchlist** - Récupération de la watchlist
9. **test_authentication_required_for_protected_routes** - Protection des routes
10. **test_complete_user_journey** - Parcours utilisateur complet

## 🚀 Exécution

### Tests unitaires (10) - Recommandé pour CI/CD

**Autonomes, rapides, fiables** - Parfaits pour l'intégration continue

```bash
# En local (avec Docker)
docker compose exec api pytest tests/unit/test_unit.py -v

# En CI/CD (sans Docker)
pytest tests/unit/test_unit.py -v
```

### Tests d'intégration (10) - Pour tests locaux uniquement

**Nécessitent que l'API tourne** - À exécuter manuellement en local

```bash
docker compose exec api pytest tests/test_integration.py -v
```

### Tous les tests (20)

```bash
docker compose exec api pytest tests/unit/test_unit.py tests/test_integration.py -v
```

### Avec couverture

```bash
docker compose exec api pytest tests/unit/test_unit.py --cov=app --cov-report=term-missing
```

## 🔄 CI/CD

Le workflow GitHub Actions (`.github/workflows/tests.yml`) exécute **uniquement les tests unitaires** car :
- ✅ Pas besoin de Docker ou services externes
- ✅ Rapides (~3-4 secondes)
- ✅ Fiables et reproductibles
- ✅ Couvrent la logique métier essentielle

Les tests d'intégration sont pour la **validation manuelle en local**.

## 📝 Exemple de test unitaire

```python
def test_create_user_with_password_hash(db):
    # Arrange
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    # Act
    user = create_user(db, user_data)
    
    # Assert
    assert user.id is not None
    assert verify_password("password123", user.hashed_password) is True
```

## 📝 Exemple de test d'intégration

```python
def test_user_registration(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
```
