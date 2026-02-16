from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.schemas import (
    DecryptRequest,
    DecryptResponse,
    EncryptRequest,
    EncryptResponse,
    ExecuteSecureQueryRequest,
    ExecuteSecureQueryResponse,
    OptimizeQueryRequest,
    OptimizeQueryResponse,
)
from backend.database.db import get_db
from backend.database.models import EncryptedRecord
from backend.encryption.he_engine import HomomorphicEncryptionEngine
from backend.ml_models.gnn_query_optimizer import QueryOptimizationService
from backend.ml_models.noise_model import NoisePredictionService
from backend.ml_models.rl_optimizer import RLOptimizerService
from backend.optimizer.query_engine import SecureQueryEngine
from backend.services.benchmark_service import BenchmarkService

router = APIRouter()
he_engine = HomomorphicEncryptionEngine()
query_opt = QueryOptimizationService.build()
noise_model = NoisePredictionService.with_default_weights()
rl_opt = RLOptimizerService()
query_engine = SecureQueryEngine(he_engine)
benchmark_service = BenchmarkService(he_engine)


@router.post("/encrypt", response_model=EncryptResponse)
def encrypt_payload(payload: EncryptRequest, db: Session = Depends(get_db)):
    encrypted = he_engine.encrypt(payload.values)
    row = EncryptedRecord(label=payload.label, ciphertext=encrypted.ciphertext, context_blob=encrypted.context_blob)
    db.add(row)
    db.commit()
    db.refresh(row)
    return EncryptResponse(record_id=row.id, ciphertext=row.ciphertext)


@router.post("/decrypt", response_model=DecryptResponse)
def decrypt_payload(payload: DecryptRequest, db: Session = Depends(get_db)):
    row = db.query(EncryptedRecord).filter(EncryptedRecord.ciphertext == payload.ciphertext).first()
    if not row:
        raise HTTPException(status_code=404, detail="Ciphertext not found")
    values = he_engine.decrypt(row.ciphertext, row.context_blob)
    return DecryptResponse(values=values)


@router.post("/optimize-query", response_model=OptimizeQueryResponse)
def optimize_query(payload: OptimizeQueryRequest):
    q = query_opt.optimize(payload.sql_query)
    rec = rl_opt.recommend(payload.complexity, q["predicted_noise_growth"])
    return OptimizeQueryResponse(**q, recommended_he_params=rec)


@router.post("/execute-secure-query", response_model=ExecuteSecureQueryResponse)
def execute_secure_query(payload: ExecuteSecureQueryRequest, db: Session = Depends(get_db)):
    try:
        result = query_engine.execute(db, payload.ids, payload.operation, payload.vector)
        return ExecuteSecureQueryResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/noise-prediction")
def noise_prediction(query_complexity: float = 1.0, depth: float = 2.0, poly_modulus_degree: float = 8192):
    features = [query_complexity, depth, poly_modulus_degree / 8192.0, query_complexity * depth]
    pred = noise_model.predict(features)
    return {"predicted_noise": pred, "features": features}


@router.get("/benchmark")
def benchmark():
    return benchmark_service.run()
