"""Pydantic schemas for API."""
from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    """Input schema for fraud prediction."""
    amount: float = Field(..., ge=0, description="Transaction amount")
    type: str = Field(..., description="Transaction type: PAYMENT, TRANSFER, CASH_OUT, CASH_IN, DEBIT")
    old_balance: float = Field(..., ge=0, description="Old balance (origin)")
    new_balance: float = Field(..., ge=0, description="New balance (origin)")
    step: int = Field(..., ge=1, le=744, description="Time step (1-744)")


class PredictionResponse(BaseModel):
    """Response schema for fraud prediction."""
    prediction: str = Field(..., description="FRAUD or SAFE")
    confidence: float = Field(..., description="Model confidence (0-1)")
    is_fraud: bool = Field(..., description="Boolean fraud indicator")
