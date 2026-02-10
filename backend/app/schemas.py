from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LookupRequest(BaseModel):
    reg_no: str = Field(..., min_length=3, max_length=32)


class LookupResponse(BaseModel):
    status: str
    reg_no: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    registration_status: Optional[str] = None


class OtpRequest(BaseModel):
    reg_no: str = Field(..., min_length=3, max_length=32)
    phone_number: str = Field(..., min_length=7, max_length=32)


class OtpRequestResponse(BaseModel):
    status: str
    reg_no: str
    phone_number: str
    otp_expires_at: str


class OtpVerifyRequest(BaseModel):
    reg_no: str = Field(..., min_length=3, max_length=32)
    otp_code: str = Field(..., min_length=4, max_length=4)


class OtpVerifyResponse(BaseModel):
    status: str
    attempt_count: Optional[int] = None


class EventRequest(BaseModel):
    event_type: str = Field(..., min_length=3, max_length=64)
    reg_no: Optional[str] = None
    details: str = Field(..., min_length=1)


class EventResponse(BaseModel):
    status: str
    created_at: datetime
