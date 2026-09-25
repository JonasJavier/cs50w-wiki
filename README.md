<div align="center">

# 📚 Wikiverse

### The encyclopedia anyone can read & write

> Originally completed for Harvard's *CS50's Web Programming with Python and JavaScript* and later rebuilt into the production-oriented full-stack application documented here.

A modern, full-stack, production-ready Wikipedia-style encyclopedia.
Built with **Django REST Framework**, **PostgreSQL**, **Redis** on the backend and
**React 19 + Vite + TypeScript + Tailwind** on the frontend.

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-A30000?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

</div>

---

## ✨ Features

- **📖 Read & write articles** in Markdown, with live preview and syntax-highlighted code.
- **🕓 Full revision history** — every edit is snapshotted; browse and compare past versions.
- **🔎 Full-text search** powered by PostgreSQL (`SearchVector` + `SearchRank`).
- **🗂️ Categories** with color theming and per-category browsing.
- **🔐 JWT authentication** — register, log in, and edit collaboratively (wiki-style).
- **⚡ Redis caching** for aggregate site stats and fast reads.
- **🌓 Light / dark mode** that respects the system preference.
- **📱 Fully responsive**, accessible UI with loading skeletons and graceful empty states.
- **📑 Auto-generated OpenAPI docs** (Swagger UI + ReDoc) via `drf-spectacular`.
- **🧪 Tested** (pytest) and **linted** (ruff + ESLint), with **CI** on every push.

## 🏗️ Architecture

```
┌──────────────┐      HTTP/JSON      ┌──────────────────┐      ┌────────────┐
│  React 19    │  ───────────────▶   │  Django + DRF    │ ───▶ │ PostgreSQL │
│  Vite + TS   │   JWT Bearer auth   │  REST API        │      └────────────┘
│  Tailwind    │  ◀───────────────   │                  │ ───▶ ┌────────────┐
└──────────────┘                     └──────────────────┘      │   Redis    │
   nginx (prod)                          gunicorn (prod)        └────────────┘
```

```
.
├── backend/                 # Django + DRF API
│   ├── config/              # settings, urls, wsgi/asgi (12-factor, env-driven)
│   └── apps/
│       ├── accounts/        # custom user, JWT auth, profiles
│       ├── articles/        # articles, categories, revisions, search, stats
│       └── common/          # pagination, health check, shared utils
├── frontend/                # React + Vite + TypeScript SPA
│   └── src/
│       ├── api/             # TanStack Query data hooks
│       ├── components/      # UI, layout & article components
│       ├── lib/             # api client, types, utils
│       ├── pages/           # route pages
│       └── store/           # Zustand (auth + theme)
├── docker-compose.yml       # local dev stack (hot reload)
└── docker-compose.prod.yml  # production-like stack (nginx + gunicorn)
```

## 🚀 Quick start (Docker)

The only prerequisite is **Docker** (with Compose).

```bash
git clone <your-repo-url> wikiverse
cd wikiverse
docker compose up --build
```

That's it. The stack boots PostgreSQL + Redis, runs migrations, **seeds demo
content**, and starts both servers:

| Service        | URL                                   |
| -------------- | ------------------------------------- |
| 🖥️  Frontend    | http://localhost:5173                 |
| 🔌  API         | http://localhost:8000/api/            |
| 📑  API docs    | http://localhost:8000/api/docs/       |
| 🛠️  Django admin | http://localhost:8000/admin/          |

**Demo account:** `admin` / `adminpass123`

> Postgres and Redis are published on host ports **5433** and **6380** to avoid
> clashing with local installs.

## 🧑‍💻 Local development (without Docker)

<details>
<summary>Backend</summary>

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
# point DATABASE_URL/REDIS_URL at your local services, or use the sqlite default
python manage.py migrate
python manage.py seed
python manage.py runserver
```
</details>

<details>
<summary>Frontend</summary>

```bash
cd frontend
npm install
npm run dev
```
</details>

## 🧪 Quality

```bash
# Backend
docker compose run --rm --entrypoint "" backend pytest      # tests (23 passing)
docker compose run --rm --no-deps --entrypoint "" backend ruff check .

# Frontend
cd frontend && npm run lint && npm run build
```

## 📦 Production

```bash
echo "SECRET_KEY=$(python -c 'import secrets;print(secrets.token_urlsafe(50))')" >> .env
docker compose -f docker-compose.prod.yml up --build -d
```

nginx serves the optimized SPA build and reverse-proxies `/api` and `/admin` to
gunicorn — single origin, no CORS. `DEBUG=false` automatically enables Django's
security hardening (HSTS, secure cookies, etc.). Open http://localhost.

## 🔌 Key API endpoints

| Method            | Endpoint                              | Description                  |
| ----------------- | ------------------------------------- | --------------------------- |
| `POST`            | `/api/auth/register/`                 | Create an account           |
| `POST`            | `/api/auth/login/`                    | Obtain JWT tokens           |
| `GET`             | `/api/articles/?search=django`        | List / full-text search     |
| `GET/POST`        | `/api/articles/`                      | Read / create articles      |
| `GET/PATCH/DELETE`| `/api/articles/{slug}/`               | Article detail & edit       |
| `GET`             | `/api/articles/{slug}/revisions/`     | Edit history                |
| `GET`             | `/api/articles/random/`               | Random article              |
| `GET`             | `/api/articles/stats/`                | Site stats (Redis-cached)   |
| `GET`             | `/api/categories/`                    | Categories                  |

Explore them all interactively at **`/api/docs/`**.

## 📝 License

MIT — built as a portfolio project. Free knowledge for everyone.
