"""
Configuration pytest et fixtures communes pour les tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.movie import Movie

# Base de données de test en mémoire SQLite
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Fixture pour créer une base de données de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Fixture pour créer un client de test FastAPI"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Fixture pour créer un utilisateur de test"""
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # Créer un objet simple avec juste l'ID pour éviter DetachedInstanceError
    class UserData:
        def __init__(self, id, username, email):
            self.id = id
            self.username = username
            self.email = email
    return UserData(user.id, user.username, user.email)


@pytest.fixture
def test_admin(db):
    """Fixture pour créer un admin de test"""
    admin = User(
        username="testadmin",
        email="admin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("adminpassword123"),
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    # Créer un objet simple avec juste l'ID
    class UserData:
        def __init__(self, id, username, email):
            self.id = id
            self.username = username
            self.email = email
    return UserData(admin.id, admin.username, admin.email)


@pytest.fixture
def test_movie(db):
    """Fixture pour créer un film de test"""
    movie = Movie(
        title="Test Movie",
        description="A test movie",
        release_year=2024
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    # Créer un objet simple avec juste l'ID
    class MovieData:
        def __init__(self, id, title):
            self.id = id
            self.title = title
    return MovieData(movie.id, movie.title)


@pytest.fixture
def token_user(client, test_user):
    """Fixture pour obtenir le token d'un utilisateur normal"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def token_admin(client, test_admin):
    """Fixture pour obtenir le token d'un admin"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testadmin", "password": "adminpassword123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers_user(token_user):
    """Fixture pour les headers d'authentification utilisateur"""
    return {"Authorization": f"Bearer {token_user}"}


@pytest.fixture
def auth_headers_admin(token_admin):
    """Fixture pour les headers d'authentification admin"""
    return {"Authorization": f"Bearer {token_admin}"}
