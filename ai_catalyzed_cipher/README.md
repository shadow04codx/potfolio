# AI-Catalyzed Cipher: Machine Learning Optimization of Homomorphic Encryption for Secure Database Querying

Production-ready reference implementation with FastAPI + TenSEAL + PyTorch + PostgreSQL + React/Tailwind dashboard.

## Architecture

- **Layer 1 (Intelligence):** Query featurization + GNN-like model predicts multiplicative depth and noise growth.
- **Layer 2 (Optimization):** RL optimizer recommends homomorphic encryption parameters.
- **Layer 3 (Execution):** TenSEAL CKKS encryption engine executes secure ops and decrypts results.
- **Database Layer:** PostgreSQL + SQLAlchemy stores encrypted records and metadata.
- **Presentation Layer:** React dashboard with benchmark and noise visualization.

## Project structure

```text
ai_catalyzed_cipher/
├── backend/
├── frontend/
├── ml_training/
├── benchmarks/
├── sample_data/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick start

```bash
docker-compose up --build
```

Services:
- API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

## API Endpoints

- `POST /encrypt`
- `POST /decrypt`
- `POST /optimize-query`
- `POST /execute-secure-query`
- `GET /noise-prediction`
- `GET /benchmark`

### Example

```bash
curl -X POST http://localhost:8000/encrypt \
  -H "Content-Type: application/json" \
  -d '{"label":"demo","values":[1,2,3]}'
```

## ML training scripts

```bash
python ml_training/train_noise_model.py
python ml_training/train_gnn.py
python ml_training/train_rl_agent.py
```

## Notes on homomorphic backend

- Uses TenSEAL CKKS when available.
- Includes fallback serialization mode for environments lacking native HE libs.
- Swap in OpenFHE or Microsoft SEAL bindings in `backend/encryption/he_engine.py` for stricter production requirements.

## Benchmarking

Call `/benchmark` or see `benchmarks/benchmark_notes.md`.

## Security considerations

- Rotate keys periodically.
- Keep secret key material in HSM/KMS in production.
- Use mTLS between services.
- Add authz/authn and audit trails.
