# 🎬 CineVerse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![React](https://img.shields.io/badge/react-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)](https://github.com/NathanLecoin/cineverse/actions)

> Une plateforme moderne de critique de films développée avec React + FastAPI + PostgreSQL

**CineVerse** permet aux utilisateurs de découvrir des films, laisser des critiques, et gérer leur watchlist personnelle. Projet académique full-stack démontrant les meilleures pratiques de développement web moderne.

## ✨ Fonctionnalités

- 🎭 **Catalogue de films** avec recherche et filtres
- ⭐ **Système de notation** (1-5 étoiles) et critiques
- 📝 **Watchlist personnelle** (à voir, en cours, vus)
- 👤 **Authentification sécurisée** (JWT)
- 🔒 **Gestion des rôles** (utilisateur, admin)
- 📱 **Interface responsive** (Tailwind CSS)
- 🐳 **Déploiement Docker** (3 conteneurs)

## 🚀 Quick Start

### Prérequis
- [Docker](https://docs.docker.com/get-docker/) >= 24.0
- [Docker Compose](https://docs.docker.com/compose/install/) >= 2.20
- [Git](https://git-scm.com/downloads)

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/votre-equipe/cineverse.git
cd cineverse

# 2. Copier les variables d'environnement
cp .env.example .env

# 3. Lancer tous les services
docker compose up --build -d

# 4. Créer les tables de base de données
docker compose exec backend alembic upgrade head

# 5. Charger les données d'exemple
docker compose exec backend python scripts/seed.py
```

### Accès à l'application

- **🌐 Frontend** : [http://localhost:3000](http://localhost:3000)
- **⚡ API Backend** : [http://localhost:8000](http://localhost:8000)  
- **📚 Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **🗄️ pgAdmin** : [http://localhost:5050](http://localhost:5050) (optionnel)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Client (Navigateur)                    │
│              localhost:3000                      │
└────────────────┬────────────────────────────────┘
                 │ HTTP/HTTPS
                 ▼
┌─────────────────────────────────────────────────┐
│       Container: Frontend (React + Vite)        │
│              Port 3000                           │
└────────────────┬────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────┐
│       Container: Backend (FastAPI)              │
│              Port 8000                           │
│   ┌──────────────────────────────────┐          │
│   │  Auth JWT  │  CRUD  │  Business  │          │
│   └──────────────────────────────────┘          │
└────────────────┬────────────────────────────────┘
                 │ SQLAlchemy
                 ▼
┌─────────────────────────────────────────────────┐
│       Container: Database (PostgreSQL)          │
│              Port 5432                           │
└─────────────────────────────────────────────────┘
```

## 💻 Stack Technologique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Frontend** | React + Vite | 18.2.0 + 5.0 |
| **Backend** | FastAPI | 0.104+ |
| **Base de données** | PostgreSQL | 16 |
| **ORM** | SQLAlchemy | 2.0 |
| **Authentification** | JWT (HS256) | - |
| **Styling** | Tailwind CSS | 3.3 |
| **Tests Backend** | pytest + httpx | - |
| **Tests Frontend** | Vitest + RTL | - |
| **Containerisation** | Docker Compose | - |

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📋 Vue d'ensemble](docs/00-OVERVIEW.md) | Présentation complète du projet |
| [⚙️ Stack technique](docs/01-STACK.md) | Technologies et structure des dossiers |
| [🌐 API Contract](docs/02-API-CONTRACT.md) | Endpoints, payloads et codes de retour |
| [🗄️ Data Model](docs/03-DATA-MODEL.md) | Schéma de base de données et relations |
| [🔐 Security](docs/04-SECURITY.md) | Authentification, autorisation, CORS |
| [🧪 Testing](docs/05-TESTING.md) | Stratégie et exemples de tests |
| [🐳 Docker](docs/06-DOCKER.md) | Configuration et commandes Docker |
| [📐 Conventions](docs/07-CONVENTIONS.md) | Standards de code et Git workflow |
| [🔄 Dev Workflow](docs/08-DEV-WORKFLOW.md) | Process de développement et CI/CD |

## 🛠️ Développement

### Commandes utiles

```bash
# Backend seul (développement)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend seul (développement)
cd frontend  
npm run dev

# Tests
docker compose exec backend pytest
docker compose exec frontend npm test

# Logs en temps réel
docker compose logs -f backend
docker compose logs -f frontend

# Redémarrer un service
docker compose restart backend

# Migrations de base de données
docker compose exec backend alembic revision --autogenerate -m "Description"
docker compose exec backend alembic upgrade head
```

### Structure du projet

```
cineverse/
├── 📚 docs/                   # Documentation
├── 🐍 backend/                # API FastAPI
│   ├── app/
│   │   ├── api/v1/           # Endpoints
│   │   ├── core/             # Configuration
│   │   ├── crud/             # Opérations BDD
│   │   ├── models/           # Modèles SQLAlchemy
│   │   └── schemas/          # Schémas Pydantic
│   ├── tests/                # Tests backend
│   └── scripts/              # Utilitaires (seed, etc.)
├── ⚛️ frontend/               # App React
│   ├── src/
│   │   ├── components/       # Composants réutilisables
│   │   ├── pages/            # Pages de l'application
│   │   ├── api/              # Appels API
│   │   └── contexts/         # État global (AuthContext)
│   └── tests/                # Tests frontend
├── 🐳 docker-compose.yml      # Orchestration des services
├── 📄 .env.example           # Variables d'environnement
└── 📖 README.md              # Ce fichier
```

## 🧪 Tests

### Backend (20 tests : 10 unitaires + 10 intégration)

```bash
# Tests unitaires uniquement (pour CI/CD)
docker compose exec api pytest tests/unit/test_unit.py -v

# Tests d'intégration (local seulement)
docker compose exec api pytest tests/test_integration.py -v

# Tous les tests
docker compose exec api pytest tests/unit/test_unit.py tests/test_integration.py -v

# Avec couverture
docker compose exec api pytest tests/unit/test_unit.py --cov=app --cov-report=term-missing
```

**Note** : Le CI/CD (GitHub Actions) exécute automatiquement les **10 tests unitaires** à chaque push. Les tests d'intégration sont pour validation locale uniquement.

### Frontend (vitest)

```bash
# Tests frontend (si configurés)
docker compose exec frontend npm test
```

## 📊 Données d'exemple

Le script de seed crée :
- **3 utilisateurs** : 1 admin + 2 utilisateurs normaux  
- **20-30 films** populaires avec affiches
- **Reviews d'exemple** pour démonstration
- **Entrées de watchlist** pour chaque utilisateur

```bash
# Recharger les données (supprime tout!)
docker compose exec backend python scripts/seed.py --reset
```

## 🚀 Déploiement

### Production

1. **Configurer les variables d'environnement** :
```bash
cp .env.example .env.production
# Éditer .env.production avec les vraies valeurs
```

2. **Variables critiques à changer** :
```bash
SECRET_KEY=<clé_générée_aléatoirement>
DEBUG=False
POSTGRES_PASSWORD=<mot_de_passe_fort>
CORS_ORIGINS=https://votre-domaine.com
```

3. **Déployer** :
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### CI/CD (GitHub Actions)

- ✅ Tests automatiques sur chaque push
- ✅ Build Docker sur merge vers `main`
- ✅ Vérification de sécurité (Bandit, Safety)
- 🚧 Déploiement automatique (à venir)

## 🤝 Contribution

### Workflow de développement

1. **Fork** le repository
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. **Développer** en respectant les [conventions](docs/07-CONVENTIONS.md)
4. **Tester** : `pytest` et `npm test`
5. **Commit** : Format [Conventional Commits](https://www.conventionalcommits.org/)
6. **Push** et créer une **Pull Request**

### Standards de code

- **Python** : `ruff` (linter) + `black` (formatter)
- **JavaScript** : `eslint` + `prettier`
- **Commits** : `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

## 🐛 Signaler un bug

Créer une [issue](https://github.com/votre-equipe/cineverse/issues) avec :
- Description du problème
- Étapes pour reproduire
- Environnement (OS, Docker version, etc.)
- Logs d'erreur si disponibles

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🎓 Contexte académique

**CineVerse** est un projet réalisé dans le cadre du cours **Full Stack Data** à l'ESIEE Paris (E5).

### Objectifs pédagogiques
- ✅ Développement d'une API REST avec FastAPI
- ✅ Interface utilisateur moderne avec React
- ✅ Base de données relationnelle (PostgreSQL)
- ✅ Authentification et autorisation (JWT)
- ✅ Conteneurisation avec Docker
- ✅ Tests automatisés (backend + frontend)
- ✅ Documentation technique complète
- ✅ Bonnes pratiques DevOps

### Équipe de développement
- **Backend Developer** : [Nom du développeur backend]
- **Frontend Developer** : [Nom du développeur frontend]

---

<p align="center">
  <strong>🎬 Fait avec ❤️ pour les cinéphiles 🍿</strong>
</p>