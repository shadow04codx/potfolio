from sqlalchemy import Column, DateTime, Integer, String, func
from .db import Base


class EncryptedRecord(Base):
    __tablename__ = "encrypted_records"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), nullable=False, index=True)
    ciphertext = Column(String, nullable=False)
    context_blob = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
