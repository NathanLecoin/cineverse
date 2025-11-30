# 🔐 Authentication Implementation - Instructions

## ✅ Ce qui a été ajouté

### 1. **Module de sécurité** (`app/core/security.py`)
- ✅ Hashing de mots de passe avec `bcrypt`
- ✅ Création de tokens JWT
- ✅ Décodage et validation de tokens

### 2. **Modèle User mis à jour** (`app/models/user.py`)
- ✅ Ajout de `is_active` (booléen)
- ✅ Ajout de `is_admin` (booléen)
- ✅ `hashed_password` déjà présent

### 3. **Schemas mis à jour** (`app/schemas/user.py`)
- ✅ `UserCreate` : ajout du champ `password` (min 8 caractères)
- ✅ `UserUpdate` : ajout du champ `password` (optionnel)
- ✅ `UserResponse` : ajout de `is_active` et `is_admin`
- ✅ Nouveaux schemas : `Token` et `TokenData`

### 4. **CRUD User mis à jour** (`app/crud/user.py`)
- ✅ `create_user()` : hash le mot de passe
- ✅ `authenticate_user()` : nouvelle fonction pour valider username/password
- ✅ `update_user()` : gère le hash du nouveau mot de passe

### 5. **Endpoints d'authentification** (`app/api/v1/auth.py`)
- ✅ `POST /auth/register` : inscription
- ✅ `POST /auth/login` : connexion et obtention du token
- ✅ `GET /auth/me` : profil utilisateur (protégé)
- ✅ `POST /auth/refresh` : rafraîchir le token
- ✅ `get_current_user()` : dépendance pour protéger les routes
- ✅ `get_current_active_admin()` : dépendance pour routes admin

### 6. **API principale mise à jour** (`app/api/v1/api.py`)
- ✅ Routes d'authentification incluses sous `/auth`

### 7. **Dépendances mises à jour** (`requirements.txt`)
- ✅ `python-jose[cryptography]` : JWT
- ✅ `passlib[bcrypt]` : hashing
- ✅ `python-multipart` : OAuth2 forms

---

## 🚀 Commandes pour démarrer

### 1. Reconstruire et démarrer Docker

```bash
cd /Users/nathanlecoin/Desktop/ESIEE/E5/Full\ Stack\ Data/cineverse

# Arrêter les conteneurs
docker compose down

# Supprimer le volume (pour recréer les tables avec les nouveaux champs)
docker volume rm cineverse_postgres_data

# Reconstruire l'image
docker compose build

# Démarrer les services
docker compose up -d

# Vérifier les logs
docker compose logs -f api
```

### 2. Vérifier que tout fonctionne

```bash
# Attendre 10 secondes que les services démarrent
sleep 10

# Tester l'endpoint de test
curl http://localhost:8000/api/v1/test
```

---

## 📝 Tester avec Postman/curl

### 1. **Inscription**

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nathan",
    "email": "nathan@cineverse.fr",
    "full_name": "Nathan Lecoin",
    "password": "securepassword123"
  }'
```

**Réponse attendue** :
```json
{
  "id": 1,
  "username": "nathan",
  "email": "nathan@cineverse.fr",
  "full_name": "Nathan Lecoin",
  "is_active": true,
  "is_admin": false
}
```

### 2. **Connexion**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=nathan&password=securepassword123"
```

**Réponse attendue** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYXRoYW4iLCJleHAiOjE2OTk5OTk5OTl9.xxx",
  "token_type": "bearer"
}
```

### 3. **Profil utilisateur (route protégée)**

```bash
# Remplace <TOKEN> par le token obtenu au login
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

**Réponse attendue** :
```json
{
  "id": 1,
  "username": "nathan",
  "email": "nathan@cineverse.fr",
  "full_name": "Nathan Lecoin",
  "is_active": true,
  "is_admin": false
}
```

### 4. **Test avec un mauvais token (devrait échouer)**

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer invalid-token"
```

**Réponse attendue** :
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 🔒 Protéger les routes existantes (PROCHAINE ÉTAPE)

Pour protéger les routes existantes (movies, reviews, watchlist), il faut :

### Exemple : Protéger la création de review

**Avant** (`app/api/v1/api.py`) :
```python
@api_router.post("/reviews", response_model=ReviewResponse)
async def create_new_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db, review)
```

**Après** :
```python
from app.api.v1.auth import get_current_user
from typing import Annotated

@api_router.post("/reviews", response_model=ReviewResponse)
async def create_new_review(
    review: ReviewCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    # Utiliser current_user.id au lieu de review.user_id
    return create_review(db, review)
```

---

## 📚 Documentation automatique

Une fois l'API démarrée, accède à :

- **Swagger UI** : http://localhost:8000/api/v1/docs
- **ReDoc** : http://localhost:8000/api/v1/redoc

Tu verras un **🔒 bouton "Authorize"** en haut à droite de Swagger :
1. Clique dessus
2. Entre ton token (sans le préfixe "Bearer")
3. Toutes les requêtes protégées utiliseront automatiquement ce token

---

## ✅ Checklist de validation

- [ ] Docker démarre sans erreur
- [ ] `/api/v1/test` renvoie un message de succès
- [ ] `/api/v1/auth/register` crée un utilisateur avec mot de passe haché
- [ ] `/api/v1/auth/login` renvoie un token JWT valide
- [ ] `/api/v1/auth/me` fonctionne avec le token
- [ ] `/api/v1/auth/me` échoue sans token (401)
- [ ] Le mot de passe est bien haché dans la BDD (pas en clair)

---

## 🐛 En cas de problème

### Erreur "module not found"
```bash
# Reconstruire l'image
docker compose build --no-cache
```

### Les tables n'ont pas les nouveaux champs
```bash
# Supprimer le volume et recréer
docker compose down
docker volume rm cineverse_postgres_data
docker compose up -d
```

### Logs pour debug
```bash
docker compose logs -f api
```

---

## 📊 État d'avancement

✅ **TERMINÉ** :
- Authentification JWT (login, register, refresh)
- Hash des mots de passe (bcrypt)
- Protection de route (dépendance `get_current_user`)
- Gestion des rôles (is_active, is_admin)

⏳ **PROCHAINES ÉTAPES** :
1. Protéger les routes existantes (reviews, watchlist, users)
2. Ajouter Alembic pour les migrations
3. Tests unitaires
4. Frontend

---

**Questions ou problèmes ?** Lance les commandes et dis-moi ce qui se passe ! 🚀
