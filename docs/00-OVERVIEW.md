# 00 - Vue d'ensemble - CineVerse

## 🎯 TL;DR

**CineVerse** est une plateforme web full-stack permettant aux utilisateurs de :
- Noter et critiquer des films
- Gérer une watchlist personnelle
- Découvrir les avis de la communauté

**Stack :** React + FastAPI + PostgreSQL + Docker
**Délai :** Projet académique en binôme
**Objectif :** Application conteneurisée avec authentification et tests

---

## 📊 Architecture Globale

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

---

## 🎨 Fonctionnalités Principales

### 1. Authentification
- Inscription / Connexion
- JWT tokens (access + refresh)
- Routes protégées

### 2. Gestion des Films
- Catalogue de films
- Recherche et filtres
- Détails complets (année, genre, description)

### 3. Système de Reviews
- Noter un film (1-5 étoiles)
- Écrire une critique
- Modifier/Supprimer ses critiques
- Feed des critiques récentes

### 4. Watchlist
- Ajouter des films à voir
- Marquer comme vu
- Gérer ses favoris

---

## 👥 Acteurs du Système

### Utilisateur Non-Authentifié
- Voir le catalogue de films
- Voir les critiques publiques
- S'inscrire / Se connecter

### Utilisateur Authentifié
- Toutes les actions ci-dessus +
- Noter et critiquer des films
- Gérer sa watchlist
- Modifier/supprimer ses propres critiques
- Voir son profil et statistiques

### Admin (Future)
- Ajouter/modifier des films
- Modération des critiques

---

## 📦 Livrables Attendus

### Requis Minimaux (Critères d'évaluation)
- ✅ Repo GitHub public
- ✅ README complet
- ✅ Dockerfile backend
- ✅ docker-compose.yml (min 2 services)
- ✅ Gestion d'utilisateurs
- ✅ Authentification JWT
- ✅ Routes API sécurisées
- ✅ Gestion erreurs HTTP
- ✅ Suite de tests automatisés
- ✅ Script de seed BDD

### Bonus
- pgAdmin pour debug
- Documentation API interactive (Swagger)
- Tests e2e
- CI/CD basique

---

## 🗂️ Structure du Repository

```
cineverse/
├── docs/                   # 📚 Cette documentation
├── backend/                # 🐍 API FastAPI
├── frontend/               # ⚛️ App React
├── docker-compose.yml      # 🐳 Orchestration
├── .github/                # 🤖 Workflows & guides Copilot
├── README.md               # Documentation principale
└── .env.example            # Template variables d'env
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/votre-equipe/cineverse.git
cd cineverse

# Variables d'environnement
cp .env.example .env

# Lancer tout
docker-compose up --build

# Créer les tables
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python scripts/seed.py

# Accès
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# pgAdmin: http://localhost:5050
```

---

## 📈 Roadmap

### Sprint 1 - Setup (Semaine 1)
- Infrastructure Docker
- Authentification
- CRUD Users

### Sprint 2 - Core Features (Semaine 2)
- CRUD Movies
- CRUD Reviews
- Tests backend

### Sprint 3 - Frontend (Semaine 3)
- Interface React
- Intégration API
- AuthContext

### Sprint 4 - Polish (Semaine 4)
- Tests e2e
- Documentation
- Seed script
- Présentation

---

## 🤝 Répartition du Travail

### Développeur Backend
- Models + CRUD + Routes API
- Authentification JWT
- Tests pytest
- Migrations Alembic

### Développeur Frontend
- Composants React
- Pages & routing
- Intégration API
- Tests frontend

---

## 📚 Documentation Complémentaire

- **[01-STACK.md](01-STACK.md)** - Détails techniques
- **[02-API-CONTRACT.md](02-API-CONTRACT.md)** - Endpoints
- **[03-DATA-MODEL.md](03-DATA-MODEL.md)** - BDD
- **[04-SECURITY.md](04-SECURITY.md)** - Auth & CORS
- **[05-TESTING.md](05-TESTING.md)** - Tests
- **[06-DOCKER.md](06-DOCKER.md)** - Containers
- **[07-CONVENTIONS.md](07-CONVENTIONS.md)** - Code style
- **[08-DEV-WORKFLOW.md](08-DEV-WORKFLOW.md)** - Git flow

---

## ❓ Questions Fréquentes

**Q: Pourquoi 3 conteneurs ?**
R: Séparation des responsabilités (frontend, backend, BDD) + facilite le développement en parallèle.

**Q: Pourquoi FastAPI et pas Django ?**
R: FastAPI = moderne, rapide, async, documentation auto, parfait pour APIs REST.

**Q: Pourquoi pas de Nginx ?**
R: Simplification pour le développement. En prod, on ajouterait Nginx.

**Q: JWT vs Sessions ?**
R: JWT = stateless, scalable, parfait pour APIs. Pas besoin de Redis.

---

## 📞 Contacts & Support

- **GitHub Issues** : Pour bugs et features
- **Discussions** : Pour questions générales
- **Wiki** : Documentation technique détaillée

---

**Dernière mise à jour :** Octobre 2025
**Version :** 1.0.0