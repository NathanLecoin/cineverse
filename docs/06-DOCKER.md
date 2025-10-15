# Docker
**TL;DR**: 3 services (db, api, frontend). Lancer, migrer, seed.

- up: `docker compose up -d --build`
- migrate: `docker compose exec backend alembic upgrade head`
- seed: `docker compose exec backend python scripts/seed.py`
