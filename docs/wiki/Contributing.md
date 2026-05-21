# Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes with tests where applicable
4. Run `docker compose up` and verify API + dashboard
5. Submit a pull request

## Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Seed
python -m app.seed
```

## Code Style

- Python: PEP 8, type hints on public functions
- TypeScript: strict mode, functional React components
