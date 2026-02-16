from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class EncryptRequest(BaseModel):
    label: str
    values: List[float] = Field(..., min_length=1)


class EncryptResponse(BaseModel):
    record_id: int
    ciphertext: str


class DecryptRequest(BaseModel):
    ciphertext: str


class DecryptResponse(BaseModel):
    values: List[float]


class OptimizeQueryRequest(BaseModel):
    sql_query: str
    complexity: float = 1.0


class OptimizeQueryResponse(BaseModel):
    multiplicative_depth: float
    predicted_noise_growth: float
    optimized_plan: Dict[str, Any]
    recommended_he_params: Dict[str, Any]


class ExecuteSecureQueryRequest(BaseModel):
    query: str
    operation: str = Field(..., pattern="^(sum|mean|dot)$")
    ids: List[int]
    vector: Optional[List[float]] = None


class ExecuteSecureQueryResponse(BaseModel):
    encrypted_result: str
    decrypted_result: List[float]
    metadata: Dict[str, Any]
