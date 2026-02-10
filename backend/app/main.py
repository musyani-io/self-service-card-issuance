from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI

from .crud import (
    create_otp_request,
    generate_otp,
    log_event,
    lookup_uni_student,
    verify_otp,
)
from .schemas import (
    EventRequest,
    EventResponse,
    LookupRequest,
    LookupResponse,
    OtpRequest,
    OtpRequestResponse,
    OtpVerifyRequest,
    OtpVerifyResponse,
)

load_dotenv()

app = FastAPI(title="Self-Service Card Issuance API")


def _get_int_env(key: str, default: int) -> int:
    value = os.getenv(key, str(default))
    try:
        return int(value)
    except ValueError:
        return default


@app.post("/lookup", response_model=LookupResponse)
def lookup_student(payload: LookupRequest) -> LookupResponse:
    student = lookup_uni_student(payload.reg_no)
    if student is None:
        log_event("lookup_not_found", payload.reg_no, "Student not found in UNI DB")
        return LookupResponse(status="NOT_FOUND")

    status = student.get("registration_status")
    if status == "INACTIVE":
        log_event("lookup_inactive", payload.reg_no, "Registration status inactive")
        return LookupResponse(status="INACTIVE", reg_no=student.get("reg_no"))

    log_event("lookup_success", payload.reg_no, "Lookup success")
    return LookupResponse(
        status="OK",
        reg_no=student.get("reg_no"),
        full_name=student.get("full_name"),
        phone_number=student.get("phone_number"),
        registration_status=status,
    )


@app.post("/otp/request", response_model=OtpRequestResponse)
def request_otp(payload: OtpRequest) -> OtpRequestResponse:
    expiry_hours = _get_int_env("OTP_EXPIRY_HOURS", 72)
    otp_code = generate_otp()
    result = create_otp_request(
        reg_no=payload.reg_no,
        phone_number=payload.phone_number,
        otp_code=otp_code,
        expiry_hours=expiry_hours,
    )
    log_event("otp_requested", payload.reg_no, f"OTP created (expires in {expiry_hours}h)")
    return OtpRequestResponse(**result)


@app.post("/otp/verify", response_model=OtpVerifyResponse)
def verify_otp_code(payload: OtpVerifyRequest) -> OtpVerifyResponse:
    result = verify_otp(payload.reg_no, payload.otp_code)
    status = result.get("status", "ERROR")
    log_event("otp_verify", payload.reg_no, f"OTP verify result: {status}")
    return OtpVerifyResponse(**result)


@app.post("/events", response_model=EventResponse)
def create_event(payload: EventRequest) -> EventResponse:
    log_event(payload.event_type, payload.reg_no, payload.details)
    return EventResponse(status="OK", created_at=datetime.utcnow())
