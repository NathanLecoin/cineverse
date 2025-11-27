# 🧪 Tests Postman - CineVerse API

## Configuration Préalable

### 1. Créer des Variables d'Environnement

Dans Postman, créer un environment "CineVerse" avec :

```
BASE_URL = http://localhost:8000
TOKEN_NATHAN = (vide au départ, sera rempli après login)
TOKEN_ADMIN = (vide au départ, sera rempli après login)
USER_ID_NATHAN = 1
USER_ID_ADMIN = 2
```

### 2. Obtenir les Tokens

Exécuter d'abord les requêtes de login ci-dessous pour obtenir les tokens.

---

## 🔑 Authentification

### Login Nathan (Utilisateur Normal)

```http
POST {{BASE_URL}}/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=nathan&password=securepassword123
```

**Script Post-Response (Tests tab)** :
```javascript
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.environment.set("TOKEN_NATHAN", jsonData.access_token);
});
```

---

### Login Admin

```http
POST {{BASE_URL}}/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=adminpassword123
```

**Script Post-Response** :
```javascript
pm.test("Admin login successful", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.environment.set("TOKEN_ADMIN", jsonData.access_token);
});
```

---

### Vérifier Profil (Me)

```http
GET {{BASE_URL}}/api/v1/auth/me
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("Profile retrieved", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.username).to.eql("nathan");
    pm.expect(jsonData.is_admin).to.be.false;
});
```

---

## 🎬 Tests Movies

### [PUBLIC] Liste des Films

```http
GET {{BASE_URL}}/api/v1/movies?skip=0&limit=10
```

**Tests** :
```javascript
pm.test("Movies list retrieved", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

---

### [ADMIN] Créer un Film - ÉCHEC avec User Normal

```http
POST {{BASE_URL}}/api/v1/movies
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "title": "Test Movie",
  "description": "Should fail",
  "release_year": 2024
}
```

**Tests** :
```javascript
pm.test("Non-admin cannot create movie", function () {
    pm.response.to.have.status(403);
});
```

---

### [ADMIN] Créer un Film - SUCCÈS avec Admin

```http
POST {{BASE_URL}}/api/v1/movies
Authorization: Bearer {{TOKEN_ADMIN}}
Content-Type: application/json

{
  "title": "Blade Runner 2049",
  "description": "A young blade runner discovers a secret",
  "release_year": 2017
}
```

**Tests** :
```javascript
pm.test("Admin can create movie", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.title).to.eql("Blade Runner 2049");
    pm.environment.set("LAST_MOVIE_ID", jsonData.id);
});
```

---

### [ADMIN] Modifier un Film

```http
PUT {{BASE_URL}}/api/v1/movies/{{LAST_MOVIE_ID}}
Authorization: Bearer {{TOKEN_ADMIN}}
Content-Type: application/json

{
  "title": "Blade Runner 2049 (Updated)",
  "description": "Updated description",
  "release_year": 2017
}
```

---

### [ADMIN] Supprimer un Film

```http
DELETE {{BASE_URL}}/api/v1/movies/{{LAST_MOVIE_ID}}
Authorization: Bearer {{TOKEN_ADMIN}}
```

---

## 📝 Tests Reviews

### [AUTH] Créer une Review pour Soi-Même - SUCCÈS

```http
POST {{BASE_URL}}/api/v1/reviews
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "movie_id": 1,
  "user_id": 1,
  "rating": 5,
  "comment": "Absolutely masterpiece! The special effects were stunning."
}
```

**Tests** :
```javascript
pm.test("User can create review for themselves", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.user_id).to.eql(1);
    pm.environment.set("NATHAN_REVIEW_ID", jsonData.id);
});
```

---

### [AUTH] Créer une Review pour Quelqu'un d'Autre - ÉCHEC

```http
POST {{BASE_URL}}/api/v1/reviews
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "movie_id": 1,
  "user_id": 999,
  "rating": 5,
  "comment": "Should fail"
}
```

**Tests** :
```javascript
pm.test("User cannot create review for others", function () {
    pm.response.to.have.status(403);
    pm.expect(pm.response.text()).to.include("only create reviews for yourself");
});
```

---

### [PUBLIC] Voir les Reviews d'un Film

```http
GET {{BASE_URL}}/api/v1/movies/1/reviews
```

**Tests** :
```javascript
pm.test("Anyone can view movie reviews", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

---

### [OWNER] Modifier sa Propre Review - SUCCÈS

```http
PUT {{BASE_URL}}/api/v1/reviews/{{NATHAN_REVIEW_ID}}
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "rating": 4,
  "comment": "Updated: Still great but not perfect"
}
```

**Tests** :
```javascript
pm.test("User can update their own review", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.rating).to.eql(4);
});
```

---

### [ADMIN] Admin Modifie la Review de Nathan

```http
PUT {{BASE_URL}}/api/v1/reviews/{{NATHAN_REVIEW_ID}}
Authorization: Bearer {{TOKEN_ADMIN}}
Content-Type: application/json

{
  "rating": 3,
  "comment": "Moderation by admin"
}
```

**Tests** :
```javascript
pm.test("Admin can modify any review", function () {
    pm.response.to.have.status(200);
});
```

---

### [OWNER] Supprimer sa Review

```http
DELETE {{BASE_URL}}/api/v1/reviews/{{NATHAN_REVIEW_ID}}
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("User can delete their own review", function () {
    pm.response.to.have.status(200);
});
```

---

## 📺 Tests Watchlist

### [AUTH] Ajouter un Film à sa Watchlist - SUCCÈS

```http
POST {{BASE_URL}}/api/v1/watchlist
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "user_id": 1,
  "movie_id": 1
}
```

**Tests** :
```javascript
pm.test("User can add to their watchlist", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.user_id).to.eql(1);
});
```

---

### [AUTH] Ajouter à la Watchlist de Quelqu'un d'Autre - ÉCHEC

```http
POST {{BASE_URL}}/api/v1/watchlist
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "user_id": 999,
  "movie_id": 1
}
```

**Tests** :
```javascript
pm.test("User cannot add to others' watchlist", function () {
    pm.response.to.have.status(403);
    pm.expect(pm.response.text()).to.include("your own watchlist");
});
```

---

### [OWNER] Voir sa Watchlist - SUCCÈS

```http
GET {{BASE_URL}}/api/v1/watchlist/1
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("User can view their own watchlist", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

---

### [AUTH] Voir la Watchlist d'un Autre - ÉCHEC

```http
GET {{BASE_URL}}/api/v1/watchlist/2
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("User cannot view others' watchlist", function () {
    pm.response.to.have.status(403);
});
```

---

### [ADMIN] Admin Voit N'importe Quelle Watchlist

```http
GET {{BASE_URL}}/api/v1/watchlist/1
Authorization: Bearer {{TOKEN_ADMIN}}
```

**Tests** :
```javascript
pm.test("Admin can view any watchlist", function () {
    pm.response.to.have.status(200);
});
```

---

### [OWNER] Retirer un Film de sa Watchlist

```http
DELETE {{BASE_URL}}/api/v1/watchlist/1/1
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("User can remove from their watchlist", function () {
    pm.response.to.have.status(200);
});
```

---

### [AUTH] Retirer de la Watchlist d'un Autre - ÉCHEC

```http
DELETE {{BASE_URL}}/api/v1/watchlist/2/1
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("User cannot remove from others' watchlist", function () {
    pm.response.to.have.status(403);
});
```

---

## 👤 Tests Users

### [PUBLIC] Voir un Profil Utilisateur

```http
GET {{BASE_URL}}/api/v1/users/1
```

**Tests** :
```javascript
pm.test("Anyone can view user profile", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('username');
    pm.expect(jsonData).to.not.have.property('hashed_password');
});
```

---

### [ADMIN] Liste des Utilisateurs - ÉCHEC avec User Normal

```http
GET {{BASE_URL}}/api/v1/users
Authorization: Bearer {{TOKEN_NATHAN}}
```

**Tests** :
```javascript
pm.test("Non-admin cannot list users", function () {
    pm.response.to.have.status(403);
});
```

---

### [ADMIN] Liste des Utilisateurs - SUCCÈS avec Admin

```http
GET {{BASE_URL}}/api/v1/users
Authorization: Bearer {{TOKEN_ADMIN}}
```

**Tests** :
```javascript
pm.test("Admin can list users", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

---

### [OWNER] Modifier son Propre Profil - SUCCÈS

```http
PUT {{BASE_URL}}/api/v1/users/1
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "full_name": "Nathan LeCoin - Updated",
  "email": "nathan.updated@example.com"
}
```

**Tests** :
```javascript
pm.test("User can update own profile", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.full_name).to.include("Updated");
});
```

---

### [OWNER] Modifier le Profil d'un Autre - ÉCHEC

```http
PUT {{BASE_URL}}/api/v1/users/2
Authorization: Bearer {{TOKEN_NATHAN}}
Content-Type: application/json

{
  "full_name": "Should Fail"
}
```

**Tests** :
```javascript
pm.test("User cannot update others' profile", function () {
    pm.response.to.have.status(403);
});
```

---

### [ADMIN] Admin Modifie N'importe Quel Profil

```http
PUT {{BASE_URL}}/api/v1/users/1
Authorization: Bearer {{TOKEN_ADMIN}}
Content-Type: application/json

{
  "full_name": "Modified by Admin"
}
```

**Tests** :
```javascript
pm.test("Admin can update any profile", function () {
    pm.response.to.have.status(200);
});
```

---

## 🚫 Tests Sans Authentification

### Accès Endpoint Protégé Sans Token

```http
POST {{BASE_URL}}/api/v1/watchlist
Content-Type: application/json

{
  "user_id": 1,
  "movie_id": 1
}
```

**Tests** :
```javascript
pm.test("Protected endpoint requires authentication", function () {
    pm.response.to.have.status(401);
    pm.expect(pm.response.text()).to.include("Not authenticated");
});
```

---

## 🔄 Tests Token Invalide

### Utiliser un Token Expiré/Invalide

```http
GET {{BASE_URL}}/api/v1/auth/me
Authorization: Bearer invalid_token_here
```

**Tests** :
```javascript
pm.test("Invalid token rejected", function () {
    pm.response.to.have.status(401);
});
```

---

## 📊 Collection Runner

Pour exécuter tous les tests automatiquement dans Postman :

1. Organiser les requêtes dans une Collection "CineVerse Tests"
2. Ordonner les requêtes :
   - Login (Nathan & Admin)
   - Tests Public
   - Tests Authenticated
   - Tests Owner
   - Tests Admin
   - Tests Negative (échecs attendus)
3. Cliquer sur "Run Collection"
4. Vérifier que tous les tests passent (vert)

---

## ✅ Résultats Attendus

**Tests qui doivent RÉUSSIR (200 OK)** :
- 2 logins (nathan + admin)
- Endpoints publics sans auth
- Utilisateur créant sa review
- Utilisateur modifiant sa review
- Utilisateur gérant sa watchlist
- Admin accédant à toutes les ressources

**Tests qui doivent ÉCHOUER** :
- 401 : Accès protégé sans token
- 403 : User tentant des actions admin
- 403 : User modifiant les ressources d'un autre
- 403 : User créant review pour un autre

---

## 🎯 Checklist de Validation

- [ ] Login nathan fonctionne
- [ ] Login admin fonctionne
- [ ] Endpoints publics accessibles sans auth
- [ ] Endpoints protégés refusent accès sans token
- [ ] User peut créer sa review
- [ ] User ne peut pas créer review pour autrui
- [ ] User peut modifier sa review
- [ ] User ne peut pas modifier review d'autrui
- [ ] Admin peut modifier toutes les reviews
- [ ] User peut gérer sa watchlist
- [ ] User ne peut pas modifier watchlist d'autrui
- [ ] Admin peut voir toutes les watchlists
- [ ] User ne peut pas créer de film
- [ ] Admin peut créer/modifier/supprimer des films
- [ ] User ne peut pas voir liste utilisateurs
- [ ] Admin peut voir liste utilisateurs
