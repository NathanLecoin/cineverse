# 🔐 04 - Security

**TL;DR**: JWT HS256, access 30 min, endpoints protégés via Bearer, roles user/admin.

---

## 🔒 Authentification JWT

### Configuration
- **Algorithme** : HS256 (HMAC with SHA-256)
- **Durée de vie** : 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Secret** : Clé de 32+ caractères (variable `SECRET_KEY`)
- **Library** : `python-jose[cryptography]`

### Format du token
```json
{
  "sub": "user@example.com",
  "exp": 1697284800,
  "iat": 1697283000,
  "role": "user"
}
```

### Usage dans les requêtes
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔐 Hash des mots de passe

### Configuration
- **Library** : `passlib[bcrypt]`
- **Rounds** : 12 (par défaut bcrypt)
- **Salage** : Automatique avec bcrypt

### Implémentation
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hasher
hashed = pwd_context.hash("password123")

# Vérifier
is_valid = pwd_context.verify("password123", hashed)
```

---

## 🌐 CORS Configuration

### Origines autorisées
- **Développement** : `http://localhost:5173` (Vite dev server)
- **Preview** : `http://localhost:3000` (Vite preview)
- **Production** : À configurer selon le domaine final

### Configuration FastAPI
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Headers requis côté client
```javascript
// Axios interceptor
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
```

---

## 👥 Système de rôles

### Rôles disponibles
- **`user`** : Utilisateur standard (par défaut)
  - Créer/modifier/supprimer ses propres reviews
  - Gérer sa watchlist
  - Voir les films et reviews des autres
  
- **`admin`** : Administrateur
  - Toutes les permissions `user` +
  - Créer/modifier des films
  - Supprimer toute review (modération)
  - Accès aux statistiques globales

### Contrôle d'accès
```python
# Dependency FastAPI
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Usage dans endpoint
@app.post("/movies", dependencies=[Depends(require_admin)])
async def create_movie(movie: MovieCreate):
    # Seuls les admins peuvent créer des films
    pass
```

---

## 🛡️ Protection des endpoints

### Endpoints publics (pas d'auth)
- `GET /movies` - Catalogue public
- `GET /movies/{id}` - Détails d'un film
- `GET /reviews/recent` - Feed public des reviews
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion

### Endpoints utilisateur authentifié 🔒
- `GET /users/me` - Profil utilisateur
- `PATCH /users/me` - Modifier profil
- `POST /reviews` - Créer une review
- `PATCH /reviews/{id}` - Modifier sa review
- `DELETE /reviews/{id}` - Supprimer sa review
- `GET /watchlist` - Sa watchlist
- `POST /watchlist` - Ajouter à watchlist
- `PATCH /watchlist/{movie_id}` - Modifier statut watchlist
- `DELETE /watchlist/{movie_id}` - Retirer de watchlist

### Endpoints admin uniquement 🔒👑
- `POST /movies` - Créer un film
- `PATCH /movies/{id}` - Modifier un film
- `DELETE /movies/{id}` - Supprimer un film

---

## ⚠️ Vulnérabilités évitées

### Injection SQL
- ✅ **SQLAlchemy ORM** : Requêtes paramétrées automatiques
- ✅ **Validation Pydantic** : Sanitisation des entrées

### XSS (Cross-Site Scripting)
- ✅ **Pas de templating HTML** : API pure JSON
- ✅ **Frontend responsable** : Échapper les données côté React

### CSRF (Cross-Site Request Forgery)
- ✅ **JWT stateless** : Pas de cookies de session
- ✅ **SameSite** : Protection CORS stricte

### Timing attacks
- ✅ **Hash constant-time** : bcrypt natif
- ✅ **Pas de révélation d'infos** : Erreurs génériques

### Brute force
- 🚧 **À implémenter** : Rate limiting (future)
- 🚧 **À implémenter** : Lockout après N tentatives

---

## 🔧 Configuration sécurisée

### Variables d'environnement critiques
```bash
# OBLIGATOIRE à changer en production
SECRET_KEY=<généré_aléatoirement_32+_chars>

# Recommandé
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False  # En production

# Base de données
POSTGRES_PASSWORD=<mot_de_passe_fort>
```

### Génération de clé secrète
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### Checklist production
- [ ] `SECRET_KEY` unique et aléatoire
- [ ] `DEBUG=False`
- [ ] CORS limité au domaine de production
- [ ] Mots de passe BDD forts
- [ ] HTTPS obligatoire
- [ ] Rate limiting activé
- [ ] Logs de sécurité configurés

---

## 📊 Audit et monitoring

### Logs de sécurité
```python
import logging

security_logger = logging.getLogger("security")

# Login réussi
security_logger.info(f"Successful login: {user.email}")

# Tentative d'accès non autorisé
security_logger.warning(f"Unauthorized access attempt: {endpoint}")

# Validation échouée
security_logger.error(f"Validation failed: {error_details}")
```

### Métriques à surveiller
- Nombre de tentatives de login échouées
- Requêtes vers endpoints admin
- Erreurs 401/403 fréquentes
- Temps de réponse des endpoints auth

---

**Dernière mise à jour :** Octobre 2025  
**Version :** 1.0.0