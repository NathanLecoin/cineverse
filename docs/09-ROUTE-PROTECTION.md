# 🔒 Protection des Routes - CineVerse API

## 📋 Vue d'ensemble

Ce document décrit l'implémentation complète de la protection des routes avec authentification JWT et autorisation basée sur les rôles.

---

## 🛡️ Stratégie de Protection

### Endpoints Publics (pas d'authentification requise)
- `GET /api/v1/movies` - Liste des films
- `GET /api/v1/movies/{movie_id}` - Détails d'un film
- `GET /api/v1/reviews` - Liste des reviews
- `GET /api/v1/reviews/{review_id}` - Détails d'une review
- `GET /api/v1/movies/{movie_id}/reviews` - Reviews d'un film
- `GET /api/v1/users/{user_id}/reviews` - Reviews d'un utilisateur
- `GET /api/v1/users/{user_id}` - Profil public d'un utilisateur
- `GET /api/v1/users/username/{username}` - Recherche par username
- `POST /api/v1/users` - Création d'utilisateur (inscription)
- `POST /api/v1/auth/register` - Inscription (préféré)
- `POST /api/v1/auth/login` - Connexion

### Endpoints Authentifiés (JWT requis)
- `GET /api/v1/auth/me` - Profil de l'utilisateur connecté
- `POST /api/v1/auth/refresh` - Rafraîchir le token
- `POST /api/v1/reviews` - Créer une review (pour soi-même)
- `POST /api/v1/watchlist` - Ajouter un film à sa watchlist
- `GET /api/v1/watchlist/{user_id}` - Voir une watchlist (propriétaire ou admin)
- `DELETE /api/v1/watchlist/{user_id}/{movie_id}` - Retirer de sa watchlist

### Endpoints Propriétaire ou Admin
- `PUT /api/v1/users/{user_id}` - Modifier son profil (ou n'importe lequel si admin)
- `DELETE /api/v1/users/{user_id}` - Supprimer son compte (ou n'importe lequel si admin)
- `PUT /api/v1/reviews/{review_id}` - Modifier sa review (ou n'importe laquelle si admin)
- `DELETE /api/v1/reviews/{review_id}` - Supprimer sa review (ou n'importe laquelle si admin)

### Endpoints Admin Uniquement
- `GET /api/v1/users` - Liste de tous les utilisateurs
- `POST /api/v1/movies` - Créer un film
- `PUT /api/v1/movies/{movie_id}` - Modifier un film
- `DELETE /api/v1/movies/{movie_id}` - Supprimer un film

---

## 🔑 Implémentation Technique

### 1. Dependencies d'Authentification

```python
from typing import Annotated
from app.api.v1.auth import get_current_user, get_current_active_admin
from app.models.user import User

# Utilisateur authentifié
current_user: Annotated[User, Depends(get_current_user)]

# Administrateur authentifié
current_admin: Annotated[User, Depends(get_current_active_admin)]
```

### 2. Vérification de Propriété

**Pour les Reviews :**
```python
@api_router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_existing_review(
    review_id: int,
    review: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    # Récupérer la review
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Vérifier propriétaire ou admin
    if db_review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    
    return update_review(db, review_id, review)
```

**Pour la Watchlist :**
```python
@api_router.post("/watchlist", response_model=WatchlistResponse)
async def add_movie_to_watchlist(
    watchlist: WatchlistCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    # Vérifier que l'utilisateur ajoute à sa propre watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only add movies to your own watchlist")
    
    return add_to_watchlist(db, watchlist)
```

### 3. Protection Admin

```python
@api_router.post("/movies", response_model=MovieResponse)
async def create_new_movie(
    movie: MovieCreate,
    current_admin: Annotated[User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db)
):
    """Create a new movie (Admin only)"""
    return create_movie(db, movie)
```

---

## 🧪 Tests de Validation

### Prérequis

1. **Démarrer l'API** :
```bash
docker-compose up -d
```

2. **Obtenir un Token Utilisateur** :
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=nathan&password=securepassword123
```

Réponse :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

3. **Obtenir un Token Admin** :
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=adminpassword123
```

---

## ✅ Scénarios de Test

### Test 1 : Accès Public (doit fonctionner sans token)

```bash
# Liste des films
GET http://localhost:8000/api/v1/movies

# Détails d'un film
GET http://localhost:8000/api/v1/movies/1

# Liste des reviews
GET http://localhost:8000/api/v1/reviews
```

**Résultat attendu** : `200 OK` avec les données

---

### Test 2 : Endpoint Protégé Sans Token (doit échouer)

```bash
# Essayer d'ajouter à une watchlist
POST http://localhost:8000/api/v1/watchlist
Content-Type: application/json

{
  "user_id": 1,
  "movie_id": 1
}
```

**Résultat attendu** : `401 Unauthorized`
```json
{
  "detail": "Not authenticated"
}
```

---

### Test 3 : Créer une Review (doit fonctionner avec token)

```bash
POST http://localhost:8000/api/v1/reviews
Authorization: Bearer <TOKEN_NATHAN>
Content-Type: application/json

{
  "movie_id": 1,
  "user_id": 1,
  "rating": 5,
  "comment": "Excellent film !"
}
```

**Résultat attendu** : `200 OK` avec la review créée

---

### Test 4 : Créer une Review pour un Autre Utilisateur (doit échouer)

```bash
POST http://localhost:8000/api/v1/reviews
Authorization: Bearer <TOKEN_NATHAN>
Content-Type: application/json

{
  "movie_id": 1,
  "user_id": 999,  # Pas l'ID de nathan
  "rating": 5,
  "comment": "Test"
}
```

**Résultat attendu** : `403 Forbidden`
```json
{
  "detail": "You can only create reviews for yourself"
}
```

---

### Test 5 : Modifier la Review d'un Autre (doit échouer pour utilisateur normal)

```bash
# Supposons que la review ID 1 appartient à l'admin
PUT http://localhost:8000/api/v1/reviews/1
Authorization: Bearer <TOKEN_NATHAN>
Content-Type: application/json

{
  "rating": 1,
  "comment": "Modification non autorisée"
}
```

**Résultat attendu** : `403 Forbidden`
```json
{
  "detail": "Not authorized to update this review"
}
```

---

### Test 6 : Admin Peut Modifier N'importe Quelle Review

```bash
PUT http://localhost:8000/api/v1/reviews/2
Authorization: Bearer <TOKEN_ADMIN>
Content-Type: application/json

{
  "rating": 4,
  "comment": "Modération admin"
}
```

**Résultat attendu** : `200 OK` avec la review modifiée

---

### Test 7 : Créer un Film Sans Être Admin (doit échouer)

```bash
POST http://localhost:8000/api/v1/movies
Authorization: Bearer <TOKEN_NATHAN>
Content-Type: application/json

{
  "title": "Nouveau Film",
  "description": "Test",
  "release_year": 2024
}
```

**Résultat attendu** : `403 Forbidden`
```json
{
  "detail": "User is not an active admin"
}
```

---

### Test 8 : Admin Peut Créer un Film

```bash
POST http://localhost:8000/api/v1/movies
Authorization: Bearer <TOKEN_ADMIN>
Content-Type: application/json

{
  "title": "The Matrix Resurrections",
  "description": "Return to the Matrix",
  "release_year": 2021
}
```

**Résultat attendu** : `200 OK` avec le film créé

---

### Test 9 : Accéder à sa Propre Watchlist

```bash
# D'abord ajouter un film
POST http://localhost:8000/api/v1/watchlist
Authorization: Bearer <TOKEN_NATHAN>
Content-Type: application/json

{
  "user_id": 1,
  "movie_id": 1
}

# Puis récupérer la watchlist
GET http://localhost:8000/api/v1/watchlist/1
Authorization: Bearer <TOKEN_NATHAN>
```

**Résultat attendu** : `200 OK` avec la liste des films

---

### Test 10 : Accéder à la Watchlist d'un Autre (doit échouer)

```bash
GET http://localhost:8000/api/v1/watchlist/2
Authorization: Bearer <TOKEN_NATHAN>
```

**Résultat attendu** : `403 Forbidden`
```json
{
  "detail": "Not authorized to view this watchlist"
}
```

---

### Test 11 : Admin Peut Voir N'importe Quelle Watchlist

```bash
GET http://localhost:8000/api/v1/watchlist/1
Authorization: Bearer <TOKEN_ADMIN>
```

**Résultat attendu** : `200 OK` avec la watchlist de l'utilisateur 1

---

### Test 12 : Liste des Utilisateurs (Admin Uniquement)

```bash
# Avec utilisateur normal (doit échouer)
GET http://localhost:8000/api/v1/users
Authorization: Bearer <TOKEN_NATHAN>

# Avec admin (doit fonctionner)
GET http://localhost:8000/api/v1/users
Authorization: Bearer <TOKEN_ADMIN>
```

**Résultats attendus** :
- Nathan : `403 Forbidden`
- Admin : `200 OK` avec la liste des utilisateurs

---

## 📊 Tableau Récapitulatif

| Endpoint | Public | User | Owner | Admin |
|----------|--------|------|-------|-------|
| GET /movies | ✅ | ✅ | ✅ | ✅ |
| POST /movies | ❌ | ❌ | ❌ | ✅ |
| PUT /movies/{id} | ❌ | ❌ | ❌ | ✅ |
| DELETE /movies/{id} | ❌ | ❌ | ❌ | ✅ |
| GET /reviews | ✅ | ✅ | ✅ | ✅ |
| POST /reviews | ❌ | ✅* | ✅* | ✅ |
| PUT /reviews/{id} | ❌ | ❌ | ✅ | ✅ |
| DELETE /reviews/{id} | ❌ | ❌ | ✅ | ✅ |
| POST /watchlist | ❌ | ✅* | ✅* | ✅ |
| GET /watchlist/{id} | ❌ | ❌ | ✅ | ✅ |
| DELETE /watchlist/{id}/{movie} | ❌ | ❌ | ✅ | ❌ |
| GET /users | ❌ | ❌ | ❌ | ✅ |
| PUT /users/{id} | ❌ | ❌ | ✅ | ✅ |
| DELETE /users/{id} | ❌ | ❌ | ✅ | ✅ |

**Légende** :
- ✅ : Accès autorisé
- ❌ : Accès refusé
- ✅* : Autorisé uniquement pour ses propres ressources

---

## 🔐 Codes d'Erreur HTTP

- **401 Unauthorized** : Token manquant ou invalide
- **403 Forbidden** : Token valide mais permissions insuffisantes
- **404 Not Found** : Ressource n'existe pas
- **422 Unprocessable Entity** : Données invalides

---

## 🚀 Prochaines Étapes

1. ✅ Protection des routes implémentée
2. ⏳ Tests de validation (à effectuer)
3. ⏳ Documentation Postman complète
4. ⏳ Tests unitaires automatisés
5. ⏳ Rate limiting et throttling
6. ⏳ CORS configuration pour le frontend
