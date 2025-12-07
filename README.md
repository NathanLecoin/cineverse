# 🎬 CineVerse

<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
    <img alt="React" src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
</p>

<p align="center">
    <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
    <img alt="Nginx" src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" />
    <img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
</p>

> Application Full Stack de gestion de films avec critiques et watchlist personnalisée

**CineVerse** est une plateforme web moderne permettant aux utilisateurs de découvrir 30 films, laisser des critiques avec notes (1-5 étoiles), et gérer leur watchlist personnelle. Projet académique ESIEE Paris E5 - Full Stack Data.

## ✨ Fonctionnalités

### Pour tous les visiteurs
- 📋 **Catalogue de 30 films** avec descriptions complètes
- 🔍 **Détails de chaque film** (titre, année, description, note moyenne)
- ⭐ **Consultation des reviews** avec notes et commentaires

### Pour les utilisateurs connectés
- 🔐 **Inscription / Connexion sécurisée** (JWT avec expiration 30 min)
- ✍️ **Créer des reviews** avec notes (1-5 étoiles) et commentaires
- 🗑️ **Supprimer ses propres reviews**
- 📚 **Gérer sa watchlist** (ajouter/retirer des films)
- 💬 **Notifications toast** pour toutes les actions

### Pour les administrateurs
- 🎬 **CRUD complet** sur les films

## 🚀 Démarrage rapide

### Prérequis
- [Docker Desktop](https://docs.docker.com/get-docker/) >= 24.0
- [Git](https://git-scm.com/downloads)

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/NathanLecoin/cineverse.git
cd cineverse

# 2. Lancer tous les services (base de données incluse)
docker compose up -d --build

# 3. Attendre 15-20 secondes que les services démarrent
# Le seed des données se fait automatiquement au premier lancement
```

### Accès

- **Frontend** : http://localhost:5173
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/api/v1/docs

### Comptes de test

```
Utilisateur Alice :
- Username: alice
- Password: alice123

Utilisateur Bob :
- Username: bob
- Password: bob123

Administrateur :
- Username: admin
- Password: adminpassword123
```



## 🏗️ Architecture

### Vue d'ensemble

```
┌─────────────────────────────────────────────────┐
│           Client (Navigateur)                    │
│              localhost                           │
└────────────────┬────────────────────────────────┘
                 │ HTTP
                 ▼
┌─────────────────────────────────────────────────┐
│    Container: Frontend (React + Nginx)          │
│              Port 5173                           │
│         Build production optimisé                │
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
│       Container: Database (PostgreSQL 15)       │
│              Port 5432                           │
│         Volume persistant                        │
└─────────────────────────────────────────────────┘
```

### Structure du projet

```
cineverse/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Routes API (36 endpoints)
│   │   ├── core/           # Config + sécurité JWT
│   │   ├── crud/           # Opérations base de données
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── schemas/        # Validation Pydantic
│   │   └── db/             # Configuration PostgreSQL
│   ├── tests/              # 20 tests automatisés
│   ├── seed_db.py          # Seed 30 films + users
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                # Variables d'environnement
│
├── frontend/               # Application React
│   ├── src/
│   │   ├── api/           # Appels API (axios)
│   │   ├── components/    # Composants réutilisables
│   │   ├── pages/         # Pages (Home, Login, etc.)
│   │   └── context/       # État global (AuthContext)
│   ├── Dockerfile         # Build multi-stage
│   ├── nginx.conf         # Config Nginx production
│   ├── package.json
│   └── .env               # Variables d'environnement
│
├── docker-compose.yml     # Orchestration 3 services
├── .github/
│   └── workflows/
│       └── tests.yml      # CI/CD automatisé
└── README.md
```

## 💻 Stack Technologique

| Composant | Technologie | Version | Description |
|-----------|-------------|---------|-------------|
| **Frontend** | React + Vite | 18.3.1 + 7.2.6 | Interface utilisateur moderne |
| **Serveur Web** | Nginx | Alpine | Serveur production (frontend) |
| **Backend** | FastAPI | 0.104.1 | API REST haute performance |
| **Base de données** | PostgreSQL | 15-alpine | Base relationnelle |
| **ORM** | SQLAlchemy | 2.0.23 | Mapping objet-relationnel |
| **Authentification** | JWT (HS256) | python-jose | Tokens sécurisés (30 min) |
| **Hashing** | Bcrypt | 4.0.1 | Hash des mots de passe |
| **Routing** | React Router | 7.1.1 | Navigation côté client |
| **HTTP Client** | Axios | 1.7.9 | Requêtes API |
| **Notifications** | react-hot-toast | 2.4.1 | Toasts élégants |
| **Tests** | pytest + pytest-cov | 7.4.3 | Tests backend |
| **CI/CD** | GitHub Actions | - | Tests automatiques |
| **Container** | Docker + Compose | 24.0+ | Orchestration services |
| **Tests Frontend** | Vitest + RTL | - |
| **Containerisation** | Docker Compose | - |

## 📖 Documentation

La documentation complète du projet était disponible dans le dossier `docs/` (exclu du versioning).

Pour comprendre l'architecture et les choix techniques, référez-vous à ce README et aux commentaires dans le code.

## 🛠️ Développement

### Commandes utiles

```bash
# Démarrer tous les services
docker compose up -d

# Backend seul (développement local, hors Docker)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend seul (développement local, hors Docker)
cd frontend
npm run dev

# Logs en temps réel
docker compose logs -f api
docker compose logs -f frontend

# Redémarrer un service
docker compose restart api

# Arrêter et nettoyer
docker compose down -v  # -v supprime les volumes (attention: perte de données)
```

**Note** : Le seed de données s'exécute automatiquement via `entrypoint.sh` au premier démarrage.

## 🧪 Tests

### Backend (20 tests : 10 unitaires + 10 API)

```bash
# Tous les tests
docker compose exec api pytest tests/ -v

# Tests unitaires uniquement
docker compose exec api pytest tests/unit/ -v

# Tests API uniquement
docker compose exec api pytest tests/test_api.py -v

# Avec couverture de code
docker compose exec api pytest tests/ --cov=app --cov-report=term-missing
```

**Note** : Le CI/CD (GitHub Actions) exécute automatiquement les 20 tests à chaque push.

## 📊 Données d'exemple

Le seed automatique (via `entrypoint.sh`) crée :

- **30 films** avec descriptions complètes en français
- **3 utilisateurs** : admin, alice, bob (voir section Comptes de test)
- **14 reviews** avec notes de 1 à 5 étoiles
- **11 entrées de watchlist** pour démonstration

Le seed s'exécute automatiquement au premier démarrage de la base de données.

## 🚀 Déploiement

### Production

Le fichier `docker-compose.yml` principal est déjà configuré pour la production avec :

- **Frontend** : Build optimisé servi par Nginx sur port 5173
- **Backend** : FastAPI avec healthcheck
- **Database** : PostgreSQL avec volume persistant

**Variables critiques à changer en production** :

```bash
# backend/.env
SECRET_KEY=<clé_générée_aléatoirement>  # python -c "import secrets; print(secrets.token_urlsafe(32))"
CORS_ORIGINS=https://votre-domaine.com
```

### CI/CD (GitHub Actions)

- ✅ Tests automatiques sur chaque push
- ✅ Build Docker vérifié
- ✅ Coverage de code

## 🤖 Utilisation de l'IA générative

Dans le cadre de ce projet académique, l'intelligence artificielle générative a été utilisée pour accélérer certains aspects du développement :

### Tests Backend

- **Formulation des cas de test** : Assistance pour structurer les 20 tests pytest (unitaires et API)
- **Couverture des scénarios** : Suggestions de cas limites et edge cases à tester
- **Raison** : Améliorer la qualité et l'exhaustivité de la suite de tests

### Base de données

- **Génération des données de seed** : Les 30 films avec descriptions complètes en français ont été générés via IA
- **Raison** : La création manuelle de données réalistes était trop fastidieuse et chronophage pour des données de démonstration
- **Contenu généré** : Titres de films, descriptions détaillées, années de sortie, genres

### Développement Frontend React

- **Assistance significative** : Implémentation des composants et de l'architecture React
- **Raison** : Connaissance limitée du framework React au début du projet
- **Composants assistés** : 
  - `MovieCard`, `MovieGrid` : Affichage des films
  - `ReviewForm`, `ReviewList`, `StarRating` : Système de reviews
  - `Navbar`, `NotFound` : Navigation et gestion d'erreurs
- **Concepts appris avec l'IA** : 
  - Hooks React (useState, useEffect, useContext, useNavigate)
  - Props et composition de composants
  - React Router (routing côté client)
  - Context API pour la gestion de l'authentification
  - Intercepteurs axios pour JWT
  - Notifications toast

### Déclaration d'intégrité académique

- **Décisions architecturales** : Toutes les décisions importantes ont été prises par l'équipe de développement (choix des technologies, structure des APIs, modèles de données, sécurité)
- **Code review** : L'ensemble du code généré par IA a été relu, testé, compris et adapté aux besoins spécifiques du projet
- **Apprentissage** : L'IA a servi d'outil pédagogique pour comprendre les patterns modernes de React et les bonnes pratiques FastAPI
- **Tests** : 20/20 tests passent avec succès, validant la qualité du code

**Outils utilisés** : GitHub Copilot, ChatGPT (explications techniques et débogage)

## 🤝 Contribution

### Workflow de développement

1. **Fork** le repository
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. **Développer** en respectant les conventions du projet
4. **Tester** : `docker compose exec api pytest tests/`
5. **Commit** : Format [Conventional Commits](https://www.conventionalcommits.org/)
6. **Push** et créer une **Pull Request**

### Standards de code

- **Python** : PEP 8, type hints, docstrings
- **JavaScript** : ESLint configuré dans le projet
- **Commits** : `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

## 🐛 Signaler un bug

Créer une issue GitHub avec :

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

### Note sur le développement

Le dernier commit a été retardé en raison d'un problème de configuration des ports Docker pour le frontend. Le conteneur Nginx nécessitait un mapping correct (5173:80) et l'injection de la variable d'environnement `VITE_API_URL` au moment du build pour permettre la communication avec l'API backend.

## 👨‍🎓 Auteurs

**Nathan LECOIN**  

ESIEE Paris – DSIA (E5)  
📫 nathan.lecoin@edu.esiee.fr

---

**🎬 Fait avec ❤️ pour les cinéphiles 🍿**
