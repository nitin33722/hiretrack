# HireTrack — Complete Build Summary

## What We Built
A job board platform using microservices architecture with Python FastAPI, PostgreSQL, and React.

---

## Architecture
```
React Frontend (5173)
        ↓
API Gateway (8000)
        ↓
Auth Service (8001) — PostgreSQL DB 1
Job Service  (8002) — PostgreSQL DB 2
App Service  (8003) — PostgreSQL DB 3
File Service (8004) — No DB (local storage)
```

---

## Services Built

### Auth Service (8001) — COMPLETE
- User registration and login
- JWT token creation and verification
- Internal `/auth/verify-token` endpoint called by other services
- Internal `/auth/users/{id}` endpoint
- Pydantic v2 schemas with `model_validate`
- bcrypt password hashing
- Alembic migrations
- PostgreSQL running on Docker port 5432

### File Service (8004) — COMPLETE
- Abstract storage backend pattern (Local/S3)
- File upload, download, delete endpoints
- MIME type and file size validation
- UUID-based file naming
- Internal secret authentication
- No database — stateless service

### Job Service (8002) — COMPLETE
- Calls Auth Service to verify JWTs (no local JWT decoding)
- Dual-role `/jobs` endpoint — recruiters see own jobs, candidates see all
- Search by title/location with pagination
- CRUD for job postings with ownership verification
- Internal `/jobs/{id}/exists` endpoint for Application Service
- Internal `/jobs/batch` endpoint for response enrichment
- `HTTPBearer(auto_error=False)` for optional authentication
- PostgreSQL running on Docker port 5433
- Migration written manually (autogenerate was empty)

### Application Service (8003) — COMPLETE
- Calls Auth, Job, and File services
- Duplicate application prevention
- Resume upload via File Service
- Response enrichment with job details (batch fetch)
- Recruiter ownership verification via Job Service
- Status tracking: pending → reviewed → accepted → rejected
- PostgreSQL running on Docker port 5434

### API Gateway (8000) — COMPLETE
- Generic proxy forwarding all requests
- Multipart file upload handling
- Rate limiting with slowapi
- Request logging with unique request IDs
- Aggregated `/health/all` endpoint
- CORS configured only here (not on individual services)

### React Frontend (5174) — COMPLETE
- Vite 4.4.0 (Node 18 compatible)
- Axios with JWT interceptor
- AuthContext with jwt-decode
- Protected routes with role checking
- Pages: Login, Register, Jobs, JobDetail, Apply, PostJob, RecruiterDashboard, CandidateDashboard
- StatusBadge component with color coding
- `/jobs/post` route placed before `/jobs/:id` to avoid conflict

---

## Key Bugs Fixed During Build

1. Auth Service — `create_at` typo in schema (should be `created_at`)
2. Auth Service — `verify-token` reading token as query param instead of request body — fixed with Pydantic request model
3. Job Service — `DATBASE_URL` typo in config
4. Job Service — `HTTPBearer(auto_error=False)` needed for public endpoints
5. File Service — `.env` not being read — added default values to config
6. File Service — `get_storage_backend()` returning class instead of instance (missing `()`)
7. File Service — `filename` vs `file_name` schema mismatch
8. Application Service — `job_exits` typo (should be `job_exists`)
9. Application Service — wrong URL `verify_token` (underscore) instead of `verify-token` (hyphen)
10. Gateway — multipart form data needed special handling
11. Frontend — `Apply.jsx` had `JobDetail` content (files got swapped)
12. Frontend — `/jobs/post` route conflicting with `/jobs/:id`
13. Frontend — CORS missing port 5174

---

## Internal Secret
All services share the same `INTERNAL_SECRET` for service-to-service authentication:
```
dev-internal-secret-for-local-testing
```

---

## Docker Containers Running
```
hiretrack-auth-db   PostgreSQL   port 5432   user: auth_user   db: hiretrack_auth
hiretrack-job-db    PostgreSQL   port 5433   user: job_user    db: hiretrack_jobs
hiretrack-app-db    PostgreSQL   port 5434   user: app_user    db: hiretrack_apps
```

---

## Project Structure
```
HireTrack/
├── services/
│   ├── auth-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── core/
│   │   │       ├── config.py
│   │   │       ├── database.py
│   │   │       └── security.py
│   │   ├── alembic/
│   │   ├── requirements.txt
│   │   └── .env
│   ├── file-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── schemas.py
│   │   │   └── core/
│   │   │       ├── config.py
│   │   │       └── storage.py
│   │   ├── uploads/
│   │   ├── requirements.txt
│   │   └── .env
│   ├── job-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── database.py
│   │   │   │   └── auth.py
│   │   │   ├── crud/
│   │   │   │   └── jobs.py
│   │   │   └── dependencies/
│   │   │       └── auth.py
│   │   ├── alembic/
│   │   ├── requirements.txt
│   │   └── .env
│   ├── application-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── database.py
│   │   │   │   └── clients.py
│   │   │   ├── crud/
│   │   │   │   └── applications.py
│   │   │   └── dependencies/
│   │   │       └── auth.py
│   │   ├── alembic/
│   │   ├── requirements.txt
│   │   └── .env
│   └── gateway/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── core/
│       │       └── config.py
│       ├── requirements.txt
│       └── .env
└── frontend/
    ├── src/
    │   ├── api/
    │   │   ├── client.js
    │   │   ├── auth.js
    │   │   ├── jobs.js
    │   │   └── applications.js
    │   ├── context/
    │   │   └── AuthContext.jsx
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   ├── ProtectedRoute.jsx
    │   │   └── StatusBadge.jsx
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── Jobs.jsx
    │   │   ├── JobDetail.jsx
    │   │   ├── Apply.jsx
    │   │   ├── PostJob.jsx
    │   │   ├── RecruiterDashboard.jsx
    │   │   └── CandidateDashboard.jsx
    │   └── App.jsx
    ├── .env
    └── .env.production

```

---

## Commands to Start Everything Locally

```bash
# Start Docker DBs
docker start hiretrack-auth-db
docker start hiretrack-job-db
docker start hiretrack-app-db

# Terminal 1 — Auth Service
cd services/auth-service && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 — File Service
cd services/file-service && uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload

# Terminal 3 — Job Service
cd services/job-service && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 4 — Application Service
cd services/application-service && uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# Terminal 5 — Gateway
cd services/gateway && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 6 — Frontend
cd frontend && npm run dev
```

---

## End-to-End Test Commands

```bash
# Register recruiter and save token
RECRUITER_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"recruiter@test.com","password":"password123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Register candidate and save token
CANDIDATE_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"candidate@test.com","password":"password123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Post a job
curl -s -X POST "http://localhost:8000/jobs" \
  -H "Authorization: Bearer $RECRUITER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Engineer","description":"Build APIs","location":"Remote","salary_range":"100000-150000"}'

# Apply for job
curl -s -X POST "http://localhost:8000/applications" \
  -H "Authorization: Bearer $CANDIDATE_TOKEN" \
  -F "job_id=1" \
  -F "cover_letter=I am interested" \
  -F "resume=@/tmp/resume.txt"

# Check all services health
curl -s "http://localhost:8000/health/all" | python3 -m json.tool
```

---

## What's Remaining

### 1. Deployment
Render free tier only allows 1 PostgreSQL database. Three options:
- **Option A** — One DB with multiple schemas (free, stays on Render)
- **Option B** — Railway (multiple free DBs, easier for microservices)
- **Option C** — Supabase for databases + Render for services (recommended)

### 2. Docker Compose
Not yet built. Would allow running everything with one command:
```bash
docker-compose up
```

### 3. Next Steps Priority
```
1. Build Docker Compose
2. Deploy using Supabase + Render
3. Add Docker to each service
```
