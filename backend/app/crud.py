from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from sqlalchemy import text

from .db import get_kiosk_engine, get_uni_engine


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat(sep=" ")


def generate_otp() -> str:
    return f"{secrets.randbelow(10000):04d}"


def hash_otp(otp_code: str) -> str:
    return hashlib.sha256(otp_code.encode("utf-8")).hexdigest()


def lookup_uni_student(reg_no: str) -> Optional[Dict[str, Any]]:
    sql = text(
        """
        SELECT reg_no, full_name, phone_number, registration_status
        FROM uni_students
        WHERE reg_no = :reg_no
        LIMIT 1
        """
    )
    with get_uni_engine().connect() as conn:
        row = conn.execute(sql, {"reg_no": reg_no}).mappings().first()

    if row is None:
        return None

    return dict(row)


def create_otp_request(
    reg_no: str,
    phone_number: str,
    otp_code: str,
    expiry_hours: int = 72,
) -> Dict[str, Any]:
    now = datetime.utcnow().replace(microsecond=0)
    expires_at = now + timedelta(hours=expiry_hours)
    otp_hash = hash_otp(otp_code)

    invalidate_sql = text(
        """
        UPDATE kiosk_otp_requests
        SET status = 'EXPIRED', failed_at = :now
        WHERE reg_no = :reg_no AND status = 'PENDING'
        """
    )
    insert_sql = text(
        """
        INSERT INTO kiosk_otp_requests (
            reg_no, phone_number, otp_hash, otp_created_at, otp_expires_at,
            status, attempt_count, max_attempts
        ) VALUES (
            :reg_no, :phone_number, :otp_hash, :otp_created_at, :otp_expires_at,
            'PENDING', 0, 3
        )
        """
    )

    with get_kiosk_engine().begin() as conn:
        conn.execute(invalidate_sql, {"reg_no": reg_no, "now": now.isoformat(sep=" ")})
        conn.execute(
            insert_sql,
            {
                "reg_no": reg_no,
                "phone_number": phone_number,
                "otp_hash": otp_hash,
                "otp_created_at": now.isoformat(sep=" "),
                "otp_expires_at": expires_at.isoformat(sep=" "),
            },
        )

    return {
        "reg_no": reg_no,
        "phone_number": phone_number,
        "otp_expires_at": expires_at.isoformat(sep=" "),
        "status": "PENDING",
    }


def verify_otp(reg_no: str, otp_code: str) -> Dict[str, Any]:
    now = datetime.utcnow().replace(microsecond=0)
    select_sql = text(
        """
        SELECT id, otp_hash, otp_expires_at, attempt_count, max_attempts
        FROM kiosk_otp_requests
        WHERE reg_no = :reg_no AND status = 'PENDING'
        ORDER BY otp_created_at DESC
        LIMIT 1
        """
    )

    with get_kiosk_engine().begin() as conn:
        row = conn.execute(select_sql, {"reg_no": reg_no}).mappings().first()

        if row is None:
            return {"status": "NOT_FOUND"}

        if row["otp_expires_at"] < now.isoformat(sep=" "):
            conn.execute(
                text(
                    """
                    UPDATE kiosk_otp_requests
                    SET status = 'EXPIRED', failed_at = :now
                    WHERE id = :id
                    """
                ),
                {"id": row["id"], "now": now.isoformat(sep=" ")},
            )
            return {"status": "EXPIRED"}

        if row["otp_hash"] == hash_otp(otp_code):
            conn.execute(
                text(
                    """
                    UPDATE kiosk_otp_requests
                    SET status = 'VERIFIED', verified_at = :now
                    WHERE id = :id
                    """
                ),
                {"id": row["id"], "now": now.isoformat(sep=" ")},
            )
            return {"status": "VERIFIED"}

        new_attempts = int(row["attempt_count"]) + 1
        if new_attempts >= int(row["max_attempts"]):
            conn.execute(
                text(
                    """
                    UPDATE kiosk_otp_requests
                    SET status = 'FAILED', attempt_count = :attempts, failed_at = :now
                    WHERE id = :id
                    """
                ),
                {
                    "id": row["id"],
                    "attempts": new_attempts,
                    "now": now.isoformat(sep=" "),
                },
            )
            return {"status": "FAILED", "attempt_count": new_attempts}

        conn.execute(
            text(
                """
                UPDATE kiosk_otp_requests
                SET attempt_count = :attempts
                WHERE id = :id
                """
            ),
            {"id": row["id"], "attempts": new_attempts},
        )
        return {"status": "INVALID", "attempt_count": new_attempts}


def log_event(event_type: str, reg_no: Optional[str], details: str) -> None:
    sql = text(
        """
        INSERT INTO kiosk_events (event_type, reg_no, details, created_at)
        VALUES (:event_type, :reg_no, :details, :created_at)
        """
    )
    with get_kiosk_engine().begin() as conn:
        conn.execute(
            sql,
            {
                "event_type": event_type,
                "reg_no": reg_no,
                "details": details,
                "created_at": _utc_now_iso(),
            },
        )
