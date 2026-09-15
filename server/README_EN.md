### Purpose
`server/` provides a local backend (FastAPI + PostgreSQL) to achieve complete separation between local and cloud environments. After deploying this service, sensitive data such as user registration, model provider configurations, tool settings, and chat history are stored on your machine and are not uploaded to our cloud unless you explicitly configure external services (e.g., cloud model providers or remote MCP servers).

### Services Provided (Main Modules)
- Users & Accounts
  - `POST /register`: Email + password registration (local DB only)
  - `POST /login`: Email + password login; returns a locally issued token
  - `GET/PUT /user`, `/user/profile`, `/user/privacy`, `/user/current_credits`, `/user/stat`, etc.
- Model Providers (store local/cloud model access configurations)
  - `GET /providers`, `POST /provider`, `PUT /provider/{id}`, `DELETE /provider/{id}`
  - `POST /provider/prefer`: Set a preferred provider (frontend/backend will prioritize it)
- Config Center (store secrets/params required by tools/capabilities)
  - `GET /configs`, `POST /configs`, `PUT /configs/{id}`, `DELETE /configs/{id}`, `GET /config/info`
- Chat & Data
  - History, snapshots, sharing, etc. in `app/controller/chat/`, all persisted to local DB
- MCP Management (import local/remote MCP servers)
  - `GET /mcps`, `POST /mcp/install`, `POST /mcp/import/{Local|Remote}`, etc.

Note: All the above data is stored in the local PostgreSQL volume in Docker (see “Data Persistence” below). If you configure external models or remote MCP, requests go to the third-party services you specify.

---

### Quick Start (Docker)
Prerequisite: Docker Desktop installed.

1) Start services
```bash
cd server
# Copy .env.example to .env(or create .env according to .env.example)
cp .env.example .env
docker compose up -d
```

2) Start Frontend (Local Mode)
- In the project root directory, create or modify `.env.development` to enable local mode and point to the local backend:
```bash
VITE_BASE_URL=/api
VITE_USE_LOCAL_PROXY=true
VITE_PROXY_URL=http://localhost:3001
```
- Start the frontend application:
```bash
npm install
npm run dev
```

### Open API docs
- `http://localhost:3001/docs` (Swagger UI)

### Ports
- API: Host `3001` → Container `5678`
- PostgreSQL: Host `127.0.0.1:5432` → Container `5432` (localhost only)

Set `POSTGRES_PASSWORD` and `secret_key` in `server/.env` before exposing this stack beyond your machine. The compose file defaults to a local-only bind so the development password is not advertised on the LAN. `secret_key` signs local login JWTs — do not keep the example value in production.

### Cloud deploy (Railway)

The FastAPI service can run on Railway with the included `railway.toml` and `server/Dockerfile`. Required variables:

- `DATABASE_URL` / `database_url` — Postgres connection string
- `secret_key` or `SECRET_KEY` — JWT signing secret
- `PORT` — listen port (Railway injects this; keep it aligned with the public domain target port)

Health check: `GET /health` (always unprefixed, even if `url_prefix=/api`).

### Data Persistence
- DB data is stored in Docker volume `server_postgres_data` at `/var/lib/postgresql/data` inside the container
- Database migrations run automatically on container startup (see `start.sh` → `alembic upgrade head`)

### Common Commands
```bash
# List running containers
docker ps

# Stop/Start API container (keep DB)
docker stop eigent_api
docker start eigent_api

# Stop/Start all (API + DB)
docker compose stop
docker compose start

# View logs
docker logs -f eigent_api | cat
docker logs -f eigent_postgres | cat
```

---

### Developer Mode (Optional)
You can run the API locally with hot-reload while keeping the database in Docker:
```bash
# Stop API in container, keep DB
docker stop eigent_api

# Run locally (provide DB connection string)
cd server
export database_url=postgresql://postgres:123456@localhost:5432/eigent
uv run uvicorn main:api --reload --port 3001 --host 0.0.0.0
```

---

### Others
- API docs: `http://localhost:3001/docs`
- Runtime logs: `/app/runtime/log/app.log` in the container
- i18n (for developers)
```bash
uv run pybabel extract -F babel.cfg -o messages.pot .
uv run pybabel init -i messages.pot -d lang -l zh_CN
uv run pybabel compile -d lang -l zh_CN
```

For a fully offline environment, only use local models and local MCP servers, and avoid configuring any external Providers or remote MCP addresses.


