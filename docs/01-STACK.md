# ⚙️ 01-STACK.md — Stack & Outils du projet Cineverse

**TL;DR**: React + FastAPI + PostgreSQL, conteneurisé avec Docker, tests automatisés.

---

## 🎯 Objectif
Cineverse est une application **Full Stack** conteneurisée :
- **Frontend :** React (Vite)
- **Backend :** FastAPI
- **Base de données :** PostgreSQL
- **Tests :** pytest (backend) / vitest (frontend)
- **Conteneurisation :** Docker Compose (3 services : db, api, frontend)

---

## 🐍 Backend

### Technologies
- **Langage :** Python 3.12
- **Framework :** FastAPI 0.104+
- **ORM :** SQLAlchemy 2.0
- **Migration :** Alembic
- **Validation :** Pydantic v2
- **Auth :** python-jose[cryptography] (JWT)
- **Hash :** passlib[bcrypt]
- **Tests :** pytest + httpx + pytest-asyncio
- **Driver BDD :** psycopg[binary]
- **Config :** python-dotenv
- **CORS :** fastapi.middleware.cors

### Structure des dossiers
```
backend/
├── alembic/                    # Migrations de BDD
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/      # Routes par domaine
│   │       │   ├── auth.py
│   │       │   ├── movies.py
│   │       │   ├── reviews.py
│   │       │   ├── watchlist.py
│   │       │   └── users.py
│   │       └── router.py       # Router principal v1
│   ├── core/
│   │   ├── config.py           # Settings (BaseSettings)
│   │   ├── security.py         # JWT, hash, verify
│   │   └── deps.py             # Dependencies (get_db, get_current_user)
│   ├── crud/                   # Opérations CRUD
│   │   ├── crud_user.py
│   │   ├── crud_movie.py
│   │   ├── crud_review.py
│   │   └── crud_watchlist.py
│   ├── models/                 # Modèles SQLAlchemy
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── review.py
│   │   └── watchlist.py
│   ├── schemas/                # Schémas Pydantic
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── review.py
│   │   ├── watchlist.py
│   │   └── token.py
│   ├── db/
│   │   ├── base.py             # Import de tous les modèles
│   │   └── session.py          # SessionLocal, engine
│   └── main.py                 # Point d'entrée FastAPI
├── tests/
│   ├── conftest.py             # Fixtures pytest
│   ├── test_auth.py
│   ├── test_movies.py
│   ├── test_reviews.py
│   └── test_watchlist.py
├── scripts/
│   └── seed.py                 # Données initiales
├── requirements.txt
├── Dockerfile
└── alembic.ini
```

### Dépendances clés (requirements.txt)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg[binary]==3.1.13
python-dotenv==1.0.0
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Variables d'environnement (.env)
```env
# Database
DATABASE_URL=postgresql://cineverse_user:cineverse_pass@db:5432/cineverse_db
POSTGRES_USER=cineverse_user
POSTGRES_PASSWORD=cineverse_pass
POSTGRES_DB=cineverse_db

# Security
SECRET_KEY=your-secret-key-min-32-characters-please-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# App
DEBUG=True
```

### Commandes utiles
```bash
# Lancer le backend seul (dev)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Migrations
docker compose exec backend alembic upgrade head
docker compose exec backend alembic revision --autogenerate -m "description"

# Seed
docker compose exec backend python scripts/seed.py

# Tests
docker compose exec backend pytest
docker compose exec backend pytest --cov=app --cov-report=html
```

---

## ⚛️ Frontend

### Technologies
- **Framework :** React 18
- **Build Tool :** Vite 5
- **Router :** React Router v6
- **HTTP Client :** Axios
- **Styling :** Tailwind CSS 3
- **Icons :** Lucide React
- **Forms :** React Hook Form + Zod
- **State :** React Context API (AuthContext)
- **Tests :** Vitest + React Testing Library

### Structure des dossiers
```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/                    # Appels API
│   │   ├── axios.js            # Instance configurée + interceptors
│   │   ├── auth.js
│   │   ├── movies.js
│   │   ├── reviews.js
│   │   └── watchlist.js
│   ├── components/
│   │   ├── common/             # Composants réutilisables
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Card.jsx
│   │   │   └── Modal.jsx
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── movies/
│   │   │   ├── MovieCard.jsx
│   │   │   ├── MovieList.jsx
│   │   │   └── MovieDetail.jsx
│   │   ├── reviews/
│   │   │   ├── ReviewCard.jsx
│   │   │   ├── ReviewForm.jsx
│   │   │   └── StarRating.jsx
│   │   └── watchlist/
│   │       └── WatchlistButton.jsx
│   ├── contexts/
│   │   └── AuthContext.jsx     # État d'authentification global
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useMovies.js
│   │   └── useDebounce.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── MovieDetail.jsx
│   │   ├── Profile.jsx
│   │   └── Watchlist.jsx
│   ├── routes/
│   │   ├── AppRouter.jsx
│   │   └── ProtectedRoute.jsx
│   ├── utils/
│   │   ├── constants.js
│   │   └── formatters.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── .env.example
├── .env.local
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── Dockerfile
```

### Dépendances clés (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "react-hook-form": "^7.48.2",
    "zod": "^3.22.4",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "vitest": "^1.0.4",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "eslint": "^8.55.0",
    "prettier": "^3.1.1"
  }
}
```

### Variables d'environnement (.env.local)
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=CineVerse
```

### Commandes utiles
```bash
# Lancer le frontend seul (dev)
cd frontend
npm run dev

# Build production
npm run build

# Preview du build
npm run preview

# Tests
npm run test
npm run test:coverage

# Linting
npm run lint
npm run format
```

---

## 🗄️ Database

### PostgreSQL 16
- **Version :** 16-alpine
- **Port :** 5432
- **Extensions :** pg_trgm (recherche full-text future)

### Outils
- **pgAdmin 4** (optionnel, pour debug)
  - URL : http://localhost:5050
  - Email : admin@cineverse.com
  - Password : admin

---

## 🐳 Docker

### Services
```yaml
# docker-compose.yml
services:
  db:       # PostgreSQL 16
  backend:  # FastAPI (Python 3.12)
  frontend: # React (Node 20)
  pgadmin:  # pgAdmin 4 (optionnel)
```

### Ports exposés
- `3000` : Frontend (React)
- `8000` : Backend (FastAPI)
- `5432` : Database (PostgreSQL)
- `5050` : pgAdmin (optionnel)

---

## 🧪 Testing

### Backend (pytest)
- Tests unitaires des CRUD
- Tests d'intégration des endpoints
- Tests d'authentification
- Coverage minimum : **80%**

### Frontend (vitest)
- Tests unitaires des composants
- Tests d'intégration des pages
- Tests des hooks personnalisés
- Coverage minimum : **70%**

---

## 🔧 Outils de développement

### Code Quality
- **Backend :** ruff (linter), black (formatter)
- **Frontend :** eslint, prettier
- **Git hooks :** pre-commit (formatage auto)

### IDE recommandé
- **VSCode** avec extensions :
  - Python
  - Pylance
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - Docker

---

## 📦 Version Management

- **Python :** `>=3.12`
- **Node.js :** `>=20 LTS`
- **PostgreSQL :** `16`
- **Docker :** `>=24.0`
- **Docker Compose :** `>=2.20`

---

## 🚀 Quick Start

```bash
# 1. Clone le repo
git clone https://github.com/votre-equipe/cineverse.git
cd cineverse

# 2. Copier les variables d'environnement
cp .env.example .env
cp frontend/.env.example frontend/.env.local

# 3. Lancer tous les services
docker compose up --build -d

# 4. Migrations
docker compose exec backend alembic upgrade head

# 5. Seed data
docker compose exec backend python scripts/seed.py

# 6. Accès
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# pgAdmin: http://localhost:5050
```

---

**Dernière mise à jour :** Octobre 2025