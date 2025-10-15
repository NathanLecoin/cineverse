# 🗄️ 03 - Data Model

**TL;DR**: PostgreSQL, 4 tables, contraintes fortes, index pour performance.

---

## 📊 Vue d'ensemble

### Relations
```
┌─────────┐       ┌─────────┐       ┌─────────┐
│  User   │──┐ ┌──│ Review  │──────▶│  Movie  │
└─────────┘  │ │  └─────────┘       └─────────┘
             │ │                         ▲
             │ │  ┌─────────┐            │
             └─┼──│Watchlist│────────────┘
               │  └─────────┘
               │
               └─ User 1:N {Reviews, Watchlist}
```

### Contraintes principales
- **Email & Username** : Uniques par utilisateur
- **Review** : Un utilisateur ne peut reviewer qu'une fois par film
- **Watchlist** : Un film ne peut être qu'une fois dans la watchlist d'un user
- **Rating** : Entre 1 et 5 (CHECK constraint)
- **Status** : ENUM('to_watch', 'watching', 'watched')

---

## 🏗️ Tables détaillées

### `users`
```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(254) NOT NULL UNIQUE,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Contraintes
ALTER TABLE users ADD CONSTRAINT chk_users_email 
    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
    
ALTER TABLE users ADD CONSTRAINT chk_users_username_length 
    CHECK (LENGTH(username) >= 3);
    
ALTER TABLE users ADD CONSTRAINT chk_users_role 
    CHECK (role IN ('user', 'admin'));
```

**Colonnes :**
- `id` : Clé primaire auto-incrémentée
- `email` : Email unique (max 254 chars RFC 5322)
- `username` : Nom d'utilisateur unique (3-50 chars)
- `password_hash` : Hash bcrypt du mot de passe
- `role` : Rôle ('user' par défaut, 'admin')
- `created_at` : Date de création (timezone aware)
- `updated_at` : Date de dernière modification

---

### `movies`
```sql
CREATE TABLE movies (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    year            INTEGER NOT NULL,
    genre           VARCHAR(100) NOT NULL,
    poster_url      TEXT,
    description     TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour performance
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_year ON movies(year);
CREATE INDEX idx_movies_genre ON movies(genre);
CREATE INDEX idx_movies_title_year ON movies(title, year); -- Pour recherches combinées

-- Contraintes
ALTER TABLE movies ADD CONSTRAINT chk_movies_year 
    CHECK (year >= 1888 AND year <= EXTRACT(YEAR FROM CURRENT_DATE) + 5);
    
ALTER TABLE movies ADD CONSTRAINT chk_movies_title_length 
    CHECK (LENGTH(title) >= 1);

-- Index pour recherche full-text (optionnel)
CREATE INDEX idx_movies_title_gin ON movies USING gin(to_tsvector('french', title));
```

**Colonnes :**
- `id` : Clé primaire auto-incrémentée
- `title` : Titre du film (requis, max 255 chars)
- `year` : Année de sortie (1888 = premier film à aujourd'hui + 5 ans)
- `genre` : Genre principal (Action, Drama, etc.)
- `poster_url` : URL de l'affiche (optionnel)
- `description` : Synopsis du film (optionnel, TEXT illimité)
- `created_at` : Date d'ajout au catalogue
- `updated_at` : Date de dernière modification

---

### `reviews`
```sql
CREATE TABLE reviews (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    movie_id        INTEGER NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    rating          INTEGER NOT NULL,
    comment         TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Contrainte unique : un user ne peut reviewer qu'une fois par film
    CONSTRAINT unq_reviews_user_movie UNIQUE(user_id, movie_id)
);

-- Index pour performance
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_created_at ON reviews(created_at DESC); -- Pour feed récent

-- Contraintes
ALTER TABLE reviews ADD CONSTRAINT chk_reviews_rating 
    CHECK (rating >= 1 AND rating <= 5);
```

**Colonnes :**
- `id` : Clé primaire auto-incrémentée
- `user_id` : FK vers users (CASCADE DELETE)
- `movie_id` : FK vers movies (CASCADE DELETE)
- `rating` : Note de 1 à 5 étoiles (requis)
- `comment` : Commentaire textuel (optionnel)
- `created_at` : Date de création de la review
- `updated_at` : Date de dernière modification

**Contraintes spéciales :**
- `UNIQUE(user_id, movie_id)` : Empêche les reviews multiples
- `CHECK(rating BETWEEN 1 AND 5)` : Valide la note

---

### `watchlist`
```sql
CREATE TYPE watchlist_status AS ENUM ('to_watch', 'watching', 'watched');

CREATE TABLE watchlist (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    movie_id        INTEGER NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    status          watchlist_status NOT NULL DEFAULT 'to_watch',
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Contrainte unique : un film ne peut être qu'une fois dans la watchlist d'un user
    CONSTRAINT unq_watchlist_user_movie UNIQUE(user_id, movie_id)
);

-- Index pour performance
CREATE INDEX idx_watchlist_user_id ON watchlist(user_id);
CREATE INDEX idx_watchlist_movie_id ON watchlist(movie_id);
CREATE INDEX idx_watchlist_status ON watchlist(status);
CREATE INDEX idx_watchlist_user_status ON watchlist(user_id, status); -- Pour filtres
```

**Colonnes :**
- `id` : Clé primaire auto-incrémentée
- `user_id` : FK vers users (CASCADE DELETE)
- `movie_id` : FK vers movies (CASCADE DELETE)
- `status` : Statut ENUM ('to_watch', 'watching', 'watched')
- `created_at` : Date d'ajout à la watchlist

**Contraintes spéciales :**
- `UNIQUE(user_id, movie_id)` : Un film une seule fois par watchlist
- `ENUM` : Valeurs de statut contrôlées

---

## 🚀 Vues métiers (optionnel)

### Vue des statistiques par film
```sql
CREATE VIEW movie_stats AS
SELECT 
    m.id,
    m.title,
    m.year,
    COUNT(r.id) as reviews_count,
    ROUND(AVG(r.rating), 1) as avg_rating,
    COUNT(w.id) as watchlist_count
FROM movies m
LEFT JOIN reviews r ON m.id = r.movie_id
LEFT JOIN watchlist w ON m.id = w.movie_id
GROUP BY m.id, m.title, m.year;
```

### Vue du feed des reviews récentes
```sql
CREATE VIEW recent_reviews AS
SELECT 
    r.id,
    r.rating,
    r.comment,
    r.created_at,
    u.username,
    m.title as movie_title,
    m.year as movie_year,
    m.poster_url
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN movies m ON r.movie_id = m.id
ORDER BY r.created_at DESC;
```

---

## 📈 Performance & Optimisation

### Index critiques
1. **Recherche de films** : `idx_movies_title`, `idx_movies_title_gin` (full-text)
2. **Feed reviews** : `idx_reviews_created_at` (DESC)
3. **Authentification** : `idx_users_email`
4. **Watchlist par user** : `idx_watchlist_user_status`

### Requêtes optimisées fréquentes
```sql
-- Recherche de films avec pagination
SELECT * FROM movies 
WHERE title ILIKE '%dune%' 
ORDER BY title 
LIMIT 12 OFFSET 0;

-- Reviews d'un film avec infos user
SELECT r.*, u.username 
FROM reviews r 
JOIN users u ON r.user_id = u.id 
WHERE r.movie_id = $1 
ORDER BY r.created_at DESC;

-- Watchlist d'un user avec infos film
SELECT w.*, m.title, m.year, m.poster_url 
FROM watchlist w 
JOIN movies m ON w.movie_id = m.id 
WHERE w.user_id = $1 AND w.status = 'to_watch';
```

---

## 🔄 Migrations (Alembic)

### Ordre de création
1. `users` (table indépendante)
2. `movies` (table indépendante)
3. `reviews` (dépend de users + movies)
4. `watchlist` (dépend de users + movies)
5. Index et contraintes
6. Vues (optionnel)

### Script de seed recommandé
```sql
-- Users de test
INSERT INTO users (email, username, password_hash, role) VALUES
('admin@cineverse.com', 'admin', '$bcrypt_hash', 'admin'),
('john@example.com', 'johndoe', '$bcrypt_hash', 'user'),
('jane@example.com', 'janedoe', '$bcrypt_hash', 'user');

-- Films populaires (20-30 films)
INSERT INTO movies (title, year, genre, poster_url, description) VALUES
('Dune', 2021, 'Sci-Fi', 'https://...', 'Paul Atreides...'),
('Inception', 2010, 'Sci-Fi', 'https://...', 'Dom Cobb...'),
-- ... plus de films

-- Reviews exemples
INSERT INTO reviews (user_id, movie_id, rating, comment) VALUES
(2, 1, 5, 'Masterpiece of science fiction!'),
(3, 1, 4, 'Great visuals, complex story');
```

---

## 🛡️ Sécurité des données

### Contraintes appliquées
- **Email valide** : Regex pattern dans CHECK constraint
- **Username minimum** : 3 caractères minimum
- **Rating borné** : Entre 1 et 5 uniquement
- **Année réaliste** : Entre 1888 et année courante + 5
- **Rôles contrôlés** : Enum ('user', 'admin')

### Cascades
- `DELETE user` → Supprime toutes ses reviews et watchlist
- `DELETE movie` → Supprime toutes les reviews et entrées watchlist

### Pas de suppression directe
- Les films ne sont jamais supprimés (données historiques)
- Les users peuvent être désactivés plutôt que supprimés

---

**Dernière mise à jour :** Octobre 2025  
**Version :** 1.0.0