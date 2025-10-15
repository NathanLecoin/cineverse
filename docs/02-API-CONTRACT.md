# 🌐 02 - API Contract (v1)

**TL;DR**: Endpoints REST, payloads JSON, pagination, codes HTTP standards.

**Base URL :** `http://localhost:8000/api/v1`

---

## 📋 Conventions générales

### Format des réponses
- **Content-Type :** `application/json`
- **Charset :** UTF-8
- **Date format :** ISO 8601 (`2025-10-14T10:30:00Z`)

### Pagination
- **Query params :** `?page=1&limit=12`
- **Défaut :** `page=1`, `limit=12`
- **Maximum :** `limit=100`
- **Format réponse :**
```json
{
  "items": [...],
  "page": 1,
  "limit": 12,
  "total": 156,
  "pages": 13
}
```

### Codes HTTP
| Code | Signification | Usage |
|------|---------------|-------|
| 200  | OK | GET réussi |
| 201  | Created | POST réussi |
| 204  | No Content | DELETE réussi |
| 400  | Bad Request | Données invalides |
| 401  | Unauthorized | Token manquant/invalide |
| 403  | Forbidden | Accès refusé (permissions) |
| 404  | Not Found | Ressource inexistante |
| 409  | Conflict | Duplicate (email, review, etc.) |
| 422  | Unprocessable Entity | Validation Pydantic échouée |
| 500  | Internal Server Error | Erreur serveur |

### Format des erreurs
```json
{
  "detail": "Review already exists for this movie",
  "error_code": "REVIEW_DUPLICATE",
  "field": "movie_id"
}
```

### Authentification
- **Header :** `Authorization: Bearer <access_token>`
- **Token :** JWT (HS256), durée 30 minutes
- **Format :** 
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## 🔐 Authentication (`/auth`)

### `POST /auth/register`
**Description :** Inscription d'un nouvel utilisateur

**Body :**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Réponse 201 :**
```json
{
  "id": 42,
  "email": "user@example.com",
  "username": "johndoe",
  "role": "user",
  "created_at": "2025-10-14T10:30:00Z"
}
```

**Erreurs :**
- `409` : Email ou username déjà utilisé
- `422` : Validation échouée (email invalide, password trop court)

---

### `POST /auth/login`
**Description :** Connexion et obtention du JWT

**Body :**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Réponse 200 :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erreurs :**
- `401` : Email ou password incorrect

---

## 👤 Users (`/users`)

### `GET /users/me` 🔒
**Description :** Récupérer le profil de l'utilisateur connecté

**Headers :** `Authorization: Bearer <token>`

**Réponse 200 :**
```json
{
  "id": 42,
  "email": "user@example.com",
  "username": "johndoe",
  "role": "user",
  "created_at": "2025-10-14T10:30:00Z",
  "stats": {
    "reviews_count": 15,
    "watchlist_count": 8
  }
}
```

**Erreurs :**
- `401` : Token invalide ou expiré

---

### `PATCH /users/me` 🔒
**Description :** Modifier son profil

**Headers :** `Authorization: Bearer <token>`

**Body (tous optionnels) :**
```json
{
  "username": "newusername",
  "email": "newemail@example.com"
}
```

**Réponse 200 :**
```json
{
  "id": 42,
  "email": "newemail@example.com",
  "username": "newusername",
  "role": "user",
  "created_at": "2025-10-14T10:30:00Z"
}
```

**Erreurs :**
- `409` : Username ou email déjà pris
- `401` : Token invalide

---

## 🎬 Movies (`/movies`)

### `GET /movies`
**Description :** Liste des films avec recherche et filtres

**Query params (tous optionnels) :**
- `search` (string) : Recherche dans title
- `genre` (string) : Filtrer par genre (ex: "Action", "Drama")
- `year` (int) : Filtrer par année
- `page` (int, défaut=1) : Numéro de page
- `limit` (int, défaut=12, max=100) : Films par page
- `sort` (string, défaut="title") : Tri ("title", "year", "avg_rating")

**Exemple :** `/movies?search=dune&genre=Sci-Fi&page=1&limit=12`

**Réponse 200 :**
```json
{
  "items": [
    {
      "id": 3,
      "title": "Dune",
      "year": 2021,
      "genre": "Sci-Fi",
      "poster_url": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
      "description": "Paul Atreides...",
      "avg_rating": 4.3,
      "reviews_count": 289,
      "created_at": "2025-10-01T12:00:00Z"
    }
  ],
  "page": 1,
  "limit": 12,
  "total": 1,
  "pages": 1
}
```

---

### `GET /movies/{id}`
**Description :** Détails complets d'un film

**Réponse 200 :**
```json
{
  "id": 3,
  "title": "Dune",
  "year": 2021,
  "genre": "Sci-Fi",
  "poster_url": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
  "description": "Paul Atreides, brilliant and gifted young man...",
  "avg_rating": 4.3,
  "reviews_count": 289,
  "created_at": "2025-10-01T12:00:00Z",
  "recent_reviews": [
    {
      "id": 1,
      "user": {
        "id": 5,
        "username": "cinephile42"
      },
      "rating": 5,
      "comment": "Masterpiece!",
      "created_at": "2025-10-14T09:00:00Z"
    }
  ]
}
```

**Erreurs :**
- `404` : Film non trouvé

---

### `POST /movies` 🔒 (Admin only)
**Description :** Ajouter un nouveau film (admin uniquement)

**Headers :** `Authorization: Bearer <admin_token>`

**Body :**
```json
{
  "title": "Oppenheimer",
  "year": 2023,
  "genre": "Biography",
  "poster_url": "https://...",
  "description": "The story of J. Robert Oppenheimer..."
}
```

**Réponse 201 :**
```json
{
  "id": 51,
  "title": "Oppenheimer",
  "year": 2023,
  "genre": "Biography",
  "poster_url": "https://...",
  "description": "The story of...",
  "avg_rating": null,
  "reviews_count": 0,
  "created_at": "2025-10-14T10:45:00Z"
}
```

**Erreurs :**
- `403` : Utilisateur non-admin
- `409` : Film déjà existant (même titre + année)

---

## ⭐ Reviews (`/reviews`)

### `POST /reviews` 🔒
**Description :** Créer une review pour un film

**Headers :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "movie_id": 3,
  "rating": 5,
  "comment": "Absolutely stunning visuals and story!"
}
```

**Réponse 201 :**
```json
{
  "id": 128,
  "movie_id": 3,
  "user": {
    "id": 42,
    "username": "johndoe"
  },
  "rating": 5,
  "comment": "Absolutely stunning visuals and story!",
  "created_at": "2025-10-14T10:50:00Z",
  "updated_at": "2025-10-14T10:50:00Z"
}
```

**Erreurs :**
- `409` : Review déjà existante pour ce film par cet utilisateur
- `404` : Movie_id inexistant
- `422` : Rating hors de 1-5

---

### `GET /reviews/recent`
**Description :** Feed des reviews récentes (publique)

**Query params :**
- `page` (défaut=1)
- `limit` (défaut=20, max=100)

**Réponse 200 :**
```json
{
  "items": [
    {
      "id": 128,
      "movie": {
        "id": 3,
        "title": "Dune",
        "poster_url": "https://..."
      },
      "user": {
        "id": 42,
        "username": "johndoe"
      },
      "rating": 5,
      "comment": "Absolutely stunning!",
      "created_at": "2025-10-14T10:50:00Z"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1542,
  "pages": 78
}
```

---

### `GET /reviews/{id}`
**Description :** Détails d'une review spécifique

**Réponse 200 :**
```json
{
  "id": 128,
  "movie": {
    "id": 3,
    "title": "Dune",
    "year": 2021
  },
  "user": {
    "id": 42,
    "username": "johndoe"
  },
  "rating": 5,
  "comment": "Absolutely stunning!",
  "created_at": "2025-10-14T10:50:00Z",
  "updated_at": "2025-10-14T10:50:00Z"
}
```

**Erreurs :**
- `404` : Review non trouvée

---

### `PATCH /reviews/{id}` 🔒
**Description :** Modifier sa propre review

**Headers :** `Authorization: Bearer <token>`

**Body (tous optionnels) :**
```json
{
  "rating": 4,
  "comment": "Good, but not perfect"
}
```

**Réponse 200 :**
```json
{
  "id": 128,
  "movie_id": 3,
  "user": {
    "id": 42,
    "username": "johndoe"
  },
  "rating": 4,
  "comment": "Good, but not perfect",
  "created_at": "2025-10-14T10:50:00Z",
  "updated_at": "2025-10-14T11:15:00Z"
}
```

**Erreurs :**
- `403` : Pas le propriétaire de la review
- `404` : Review non trouvée
- `422` : Rating invalide

---

### `DELETE /reviews/{id}` 🔒
**Description :** Supprimer sa propre review

**Headers :** `Authorization: Bearer <token>`

**Réponse 204 :** (No Content)

**Erreurs :**
- `403` : Pas le propriétaire
- `404` : Review non trouvée

---

## 📝 Watchlist (`/watchlist`)

### `GET /watchlist` 🔒
**Description :** Récupérer sa watchlist

**Headers :** `Authorization: Bearer <token>`

**Query params :**
- `status` (optionnel) : Filtrer par "to_watch", "watching", "watched"
- `page` (défaut=1)
- `limit` (défaut=20)

**Réponse 200 :**
```json
{
  "items": [
    {
      "id": 1,
      "movie": {
        "id": 5,
        "title": "Inception",
        "year": 2010,
        "poster_url": "https://...",
        "avg_rating": 4.7
      },
      "status": "to_watch",
      "created_at": "2025-10-10T14:30:00Z"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 8,
  "pages": 1
}
```

---

### `POST /watchlist` 🔒
**Description :** Ajouter un film à sa watchlist

**Headers :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "movie_id": 5,
  "status": "to_watch"
}
```

**Réponse 201 :**
```json
{
  "id": 1,
  "movie_id": 5,
  "status": "to_watch",
  "created_at": "2025-10-14T11:00:00Z"
}
```

**Erreurs :**
- `409` : Film déjà dans la watchlist
- `404` : Movie_id inexistant
- `422` : Status invalide (doit être "to_watch", "watching", "watched")

---

### `PATCH /watchlist/{movie_id}` 🔒
**Description :** Modifier le statut d'un film dans la watchlist

**Headers :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "status": "watched"
}
```

**Réponse 200 :**
```json
{
  "id": 1,
  "movie_id": 5,
  "status": "watched",
  "created_at": "2025-10-10T14:30:00Z"
}
```

**Erreurs :**
- `404` : Film pas dans la watchlist
- `422` : Status invalide

---

### `DELETE /watchlist/{movie_id}` 🔒
**Description :** Retirer un film de sa watchlist

**Headers :** `Authorization: Bearer <token>`

**Réponse 204 :** (No Content)

**Erreurs :**
- `404` : Film pas dans la watchlist

---

## 🔄 Versioning

- **Version actuelle :** v1
- **Base path :** `/api/v1`
- **Breaking changes :** Nouvelle version (/api/v2)
- **Deprecation :** 6 mois de préavis minimum

---

**Dernière mise à jour :** Octobre 2025  
**Version :** 1.0.0