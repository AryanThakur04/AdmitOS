# AdmitOS Deployment Guide

## Option A: Docker (Local / VPS)

```bash
cd admitos
cp .env.example .env
docker compose up --build -d
docker compose exec api python -m app.seed
```

- API: `http://localhost:8000`
- Dashboard: `http://localhost:5173`

## Option B: Render.com

### 1. PostgreSQL
Create a **PostgreSQL** instance on Render. Copy the **Internal Database URL**.

### 2. Web Service (API)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment**:
  - `DATABASE_URL` = Render Postgres URL
  - `SECRET_KEY` = random 32-char string
  - `CORS_ORIGINS` = your frontend URL
  - `GEMINI_API_KEY` or `OPENAI_API_KEY` (optional)

### 3. Static Site (Frontend)
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Environment**: `VITE_API_URL=https://your-api.onrender.com`

### 4. Seed (one-time)
Use Render Shell:
```bash
python -m app.seed
```

## Option C: AWS

| Component | Service |
|-----------|---------|
| API | ECS Fargate or Elastic Beanstalk |
| DB | RDS PostgreSQL |
| Frontend | S3 + CloudFront |
| Secrets | AWS Secrets Manager |

Use the provided `backend/Dockerfile` and `frontend` build output.

## Post-deploy checklist

- [ ] Run database seed
- [ ] Set `SECRET_KEY` and API keys
- [ ] Configure `CORS_ORIGINS`
- [ ] Test `/health` and `/docs`
- [ ] Import `data/sample_leads.csv` via API
