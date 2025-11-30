"""
Configuration des tests unitaires pour CineVerse

Fixtures pour les tests unitaires :
- db : Session de base de données SQLite en mémoire
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

# Configuration de la base de données de test (SQLite en mémoire)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

def pytest_configure(config):
    """
    Configuration dynamique de pytest
    Définit les marqueurs pour les tests
    """
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )


@pytest.fixture(scope="function")
def db():
    """
    Fixture pour créer une session de base de données de test
    
    Utilise SQLite en mémoire pour l'isolation des tests
    Crée les tables avant chaque test et les supprime après
    
    Yields:
        Session: Session SQLAlchemy pour les tests
    """
    # Créer l'engine de test
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
