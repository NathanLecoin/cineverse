# 🧠 Copilot — Règles & Conventions pour Cineverse

> **TL;DR**  
> Tu es un pair IA. Tu aides à modifier le code **FastAPI / React / PostgreSQL** de Cineverse  
> de manière sûre, claire et cohérente. Tu respectes **les conventions et l’architecture**.

---

## 🎯 Objectif
- Produire des modifications **petites, sûres et cohérentes**.  
- Préserver le comportement existant et la lisibilité.  
- Ne pas ajouter de dépendances sauf nécessité absolue.

---

## ⚙️ Stack
- **Backend** : FastAPI + SQLAlchemy + Alembic + Pydantic v2  
- **Frontend** : React (Vite) + Axios  
- **BDD** : PostgreSQL  
- **Tests** : pytest + httpx  
- **Conteneurs** : Docker Compose (db + api + frontend)

---

## 🧩 Principes généraux

**✅ Do**
- Petites modifications ciblées.  
- Suivre le style du code voisin.  
- Valider les données avec Pydantic.  
- Utiliser les bons codes HTTP : 400, 401, 403, 404, 409.  
- Commenter uniquement la logique complexe.  

**🚫 Don’t**
- Refactor global inutile.  
- Ajouter de dépendances sans raison.  
- Casser les API publiques.  
- Reformater un fichier complet.  

---

## 🔐 Auth & Sécurité
- JWT HS256, durée : **30 min**.  
- Password hash : `passlib[bcrypt]`.  
- CORS autorisé : `http://localhost:5173` (dev).  
- Rôles : `user` / `admin`.

---

## 🛣️ API Contract (v1)

### Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`

### Movies
- `GET /movies` (search, pagination)
- `GET /movies/{id}`
- `POST /movies` (admin)

### Reviews
- `POST /reviews` (unique par user/movie)
- `GET /reviews/recent`
- `DELETE /reviews/{id}`

---

## 🧱 Backend conventions
1. **Arborescence**
   - `models/`, `schemas/`, `crud/`, `api/v1/`

2. **CRUD**
   - Requêtes simples, une responsabilité par fonction.  
   - Exceptions avec :  
     ```py
     raise HTTPException(status_code=409, detail="Review already exists")
     ```

3. **Tests**
   - Utiliser **pytest** + **client httpx**.  
   - Exemple :
     ```py
     def test_review_duplicate(client, token, movie_id):
         r1 = client.post(
             "/api/v1/reviews",
             headers=auth(token),
             json={"movie_id": movie_id, "rating": 5},
         )
         r2 = client.post(
             "/api/v1/reviews",
             headers=auth(token),
             json={"movie_id": movie_id, "rating": 4},
         )
         assert r2.status_code == 409
     ```

---

## ⚛️ Frontend conventions
- Framework : **React (Vite)**, Axios + interceptors, Tailwind.  
- Authentification : JWT stocké dans `localStorage`.  
- Routes protégées : `<ProtectedRoute />`.  
- Base URL : `import.meta.env.VITE_API_URL`.  
- Ne jamais stocker le mot de passe en clair côté client.

---

## ✅ Checklist avant PR
- [ ] Tests passent (**pytest**, **vitest**).  
- [ ] Doc / README à jour.  
- [ ] Conventions de nommage respectées.  
- [ ] Pas de refactor global inutile.  
- [ ] Code conforme à cette charte.  

---

## 🧾 Commit convention (rappel)
Utiliser le format [Conventional Commits](https://www.conventionalcommits.org) :