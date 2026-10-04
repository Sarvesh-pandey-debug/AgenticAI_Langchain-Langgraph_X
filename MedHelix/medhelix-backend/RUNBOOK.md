# MedHelix — Command Runbook

This document contains every command you will ever need to run, manage, and debug the MedHelix backend from scratch. 

> **Important**: Always run these commands from the `medhelix-backend` folder!
> ```bash
> cd C:\Users\sar\OneDrive\Desktop\AgenticAI-X\MedHelix\medhelix-backend
> ```

---

## 🐳 1. Running with Docker (Recommended)
This spins up PostgreSQL, Redis, and the FastAPI backend all at once.

**Start the entire project:**
```bash
docker-compose up -d
```

**Stop the project:**
```bash
docker-compose down
```

**Rebuild the API container (Run this if you add new PIP packages):**
```bash
docker-compose up -d --build
```

**View live logs of the API:**
```bash
docker logs -f medhelix_api
```

---

## 💻 2. Running Locally (Without Docker API)
If you prefer to run the API directly on your Windows machine for easier debugging, while keeping the database in Docker.

**Step 1: Start just the databases in Docker:**
```bash
docker-compose up -d postgres redis
```

**Step 2: Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 4: Run the FastAPI server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🗄️ 3. Database Migrations (Alembic)
Use these when you add or change models in `app/models/`.

**Generate a new migration script (After modifying Python models):**
```bash
# If running via Docker:
docker exec -e PYTHONPATH=/app medhelix_api alembic revision --autogenerate -m "describe_your_change"

# If running locally (venv):
alembic revision --autogenerate -m "describe_your_change"
```

**Apply the migrations to the database:**
```bash
# If running via Docker:
docker exec -e PYTHONPATH=/app medhelix_api alembic upgrade head

# If running locally (venv):
alembic upgrade head
```

---

## 🔍 4. Useful Debugging Commands

**Connect directly to the PostgreSQL database:**
```bash
docker exec -it medhelix_postgres psql -U medhelix -d medhelix
# (Once inside, type \dt to see tables, \q to quit)
```

**Connect directly to Redis to check cache:**
```bash
docker exec -it medhelix_redis redis-cli
# (Once inside, type KEYS * to see cached items)
```

**Check if the API is healthy (PowerShell):**
```powershell
Invoke-RestMethod http://localhost:8000/health
```
