# Testing Strategy
**TL;DR**: pytest + httpx; tests unitaires, intégration, E2E légers.

## Cibles
- Auth: signup/login/me (+ erreurs 401/409)
- Reviews: create -> duplicate 409 -> patch/delete owner
- Movies: filtres, pagination, tri

## Ex d’un test d’endpoint (pseudo)
```py
def test_login(client, user):
    r = client.post("/api/v1/auth/login", json={"email": user.email, "password":"pass"})
    assert r.status_code == 200 and "access_token" in r.json()