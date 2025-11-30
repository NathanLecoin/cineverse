"""
Tests d'intégration essentiels - CineVerse API
10 tests couvrant les workflows critiques
"""
import pytest
from fastapi.testclient import TestClient


def test_user_registration(client):
    """Test que l'inscription d'un utilisateur fonctionne"""
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"


def test_user_login(client, test_user):
    """Test que la connexion retourne un token JWT"""
    response = client.post("/api/v1/auth/login", data={
        "username": test_user.username,
        "password": "testpassword123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user_with_token(client, auth_headers_user):
    """Test que /auth/me retourne l'utilisateur connecté"""
    response = client.get("/api/v1/auth/me", headers=auth_headers_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_list_movies_public(client, test_movie):
    """Test que la liste des films est accessible publiquement"""
    response = client.get("/api/v1/movies/")
    
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_create_movie_requires_admin(client, auth_headers_user, auth_headers_admin):
    """Test que seul un admin peut créer un film"""
    movie_data = {
        "title": "New Movie",
        "description": "Test movie",
        "release_year": 2024
    }
    
    # Utilisateur normal → 403
    response = client.post("/api/v1/movies/", json=movie_data, headers=auth_headers_user)
    assert response.status_code == 403
    
    # Admin → 200 ou 201
    response = client.post("/api/v1/movies/", json=movie_data, headers=auth_headers_admin)
    assert response.status_code in [200, 201]
    assert response.json()["title"] == "New Movie"


def test_create_review_workflow(client, auth_headers_user, test_movie):
    """Test du workflow complet de création de review"""
    review_data = {
        "user_id": 1,  # ID de test_user
        "movie_id": test_movie.id,
        "rating": 5,
        "comment": "Excellent film!"
    }
    
    response = client.post("/api/v1/reviews/", json=review_data, headers=auth_headers_user)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Excellent film!"


def test_add_movie_to_watchlist_workflow(client, auth_headers_user, test_movie):
    """Test du workflow complet d'ajout à la watchlist"""
    watchlist_data = {
        "user_id": 1,  # ID de test_user
        "movie_id": test_movie.id
    }
    
    response = client.post("/api/v1/watchlist/", json=watchlist_data, headers=auth_headers_user)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["movie_id"] == test_movie.id


def test_get_user_watchlist(client, auth_headers_user, test_movie):
    """Test de récupération de la watchlist d'un utilisateur"""
    # Ajouter un film à la watchlist
    client.post("/api/v1/watchlist/", json={
        "user_id": 1,
        "movie_id": test_movie.id
    }, headers=auth_headers_user)
    
    # Récupérer la watchlist
    response = client.get("/api/v1/watchlist/1", headers=auth_headers_user)
    
    assert response.status_code == 200
    watchlist = response.json()
    assert isinstance(watchlist, list)
    assert len(watchlist) > 0


def test_authentication_required_for_protected_routes(client):
    """Test que les routes protégées nécessitent une authentification"""
    # Sans token → 401
    response = client.post("/api/v1/reviews/", json={
        "user_id": 1,
        "movie_id": 1,
        "rating": 5,
        "comment": "Test"
    })
    assert response.status_code == 401
    
    response = client.post("/api/v1/watchlist/", json={
        "user_id": 1,
        "movie_id": 1
    })
    assert response.status_code == 401


def test_complete_user_journey(client):
    """Test du parcours complet d'un utilisateur"""
    # 1. Inscription
    register_response = client.post("/api/v1/auth/register", json={
        "username": "journeyuser",
        "email": "journey@example.com",
        "password": "password123"
    })
    assert register_response.status_code == 201
    
    # 2. Connexion
    login_response = client.post("/api/v1/auth/login", data={
        "username": "journeyuser",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Récupérer son profil
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "journeyuser"
    
    # 4. Consulter les films
    movies_response = client.get("/api/v1/movies/")
    assert movies_response.status_code == 200
