"""
Tests unitaires essentiels - CineVerse Backend
10 tests couvrant les fonctions critiques
"""
import pytest
from datetime import timedelta
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)
from app.crud.user import create_user, authenticate_user
from app.crud.movie import create_movie
from app.crud.review import create_review
from app.crud.watchlist import add_to_watchlist, is_in_watchlist
from app.schemas.user import UserCreate
from app.schemas.movie import MovieCreate
from app.schemas.review import ReviewCreate
from app.schemas.watchlist import WatchlistCreate


def test_password_hashing_and_verification():
    """Test que le hash et la vérification de mot de passe fonctionnent"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_creation_and_decoding():
    """Test que la création et le décodage de tokens JWT fonctionnent"""
    data = {"sub": "testuser", "user_id": 123}
    token = create_access_token(data, timedelta(minutes=30))
    
    assert token is not None
    
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "testuser"
    assert payload["user_id"] == 123


def test_create_user_with_password_hash(db):
    """Test que la création d'utilisateur hash le mot de passe"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    user = create_user(db, user_data)
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.hashed_password != "password123"
    assert verify_password("password123", user.hashed_password) is True


def test_authenticate_user_success_and_failure(db):
    """Test que l'authentification valide les credentials correctement"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    create_user(db, user_data)
    
    # Test authentification réussie
    authenticated = authenticate_user(db, "testuser", "password123")
    assert authenticated is not False
    assert authenticated.username == "testuser"
    
    # Test authentification échouée
    assert authenticate_user(db, "testuser", "wrongpassword") is False
    assert authenticate_user(db, "wronguser", "password123") is False


def test_create_and_get_movie(db):
    """Test que la création et récupération de film fonctionnent"""
    movie_data = MovieCreate(
        title="Test Movie",
        description="A test movie",
        release_year=2024
    )
    
    movie = create_movie(db, movie_data)
    
    assert movie.id is not None
    assert movie.title == "Test Movie"
    assert movie.release_year == 2024


def test_create_review_for_movie(db):
    """Test que la création de review pour un film fonctionne"""
    user = create_user(db, UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    ))
    movie = create_movie(db, MovieCreate(
        title="Test Movie",
        description="Test",
        release_year=2024
    ))
    
    review_data = ReviewCreate(
        user_id=user.id,
        movie_id=movie.id,
        rating=5,
        comment="Great movie!"
    )
    review = create_review(db, review_data)
    
    assert review.id is not None
    assert review.user_id == user.id
    assert review.movie_id == movie.id
    assert review.rating == 5


def test_add_movie_to_watchlist(db):
    """Test que l'ajout d'un film à la watchlist fonctionne"""
    user = create_user(db, UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    ))
    movie = create_movie(db, MovieCreate(
        title="Test Movie",
        description="Test",
        release_year=2024
    ))
    
    watchlist_data = WatchlistCreate(user_id=user.id, movie_id=movie.id)
    watchlist = add_to_watchlist(db, watchlist_data)
    
    assert watchlist.id is not None
    assert watchlist.user_id == user.id
    assert watchlist.movie_id == movie.id


def test_check_movie_in_watchlist(db):
    """Test que la vérification de présence dans la watchlist fonctionne"""
    user = create_user(db, UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    ))
    movie1 = create_movie(db, MovieCreate(title="Movie 1", description="Test", release_year=2024))
    movie2 = create_movie(db, MovieCreate(title="Movie 2", description="Test", release_year=2024))
    
    add_to_watchlist(db, WatchlistCreate(user_id=user.id, movie_id=movie1.id))
    
    assert is_in_watchlist(db, user.id, movie1.id) is True
    assert is_in_watchlist(db, user.id, movie2.id) is False


def test_watchlist_prevents_duplicates(db):
    """Test que la watchlist ne permet pas les doublons"""
    user = create_user(db, UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    ))
    movie = create_movie(db, MovieCreate(title="Test Movie", description="Test", release_year=2024))
    
    watchlist_data = WatchlistCreate(user_id=user.id, movie_id=movie.id)
    first = add_to_watchlist(db, watchlist_data)
    second = add_to_watchlist(db, watchlist_data)
    
    assert first.id == second.id


def test_password_hash_uses_salt(db):
    """Test que le hash de mot de passe utilise un salt (résultats différents)"""
    password = "testpassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2
    
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
