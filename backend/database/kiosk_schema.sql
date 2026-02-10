CREATE TABLE IF NOT EXISTS kiosk_otp_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_no TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    otp_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    otp_expires_at DATETIME NOT NULL,
    status TEXT NOT NULL,
    attempt_count INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    verified_at DATETIME,
    failed_at DATETIME
);

CREATE INDEX idx_kiosk_otp_reg_no ON kiosk_otp_requests (reg_no);
CREATE INDEX idx_kiosk_otp_phone ON kiosk_otp_requests (phone_number);
CREATE INDEX idx_kiosk_otp_expires ON kiosk_otp_requests (otp_expires_at);

CREATE TABLE IF NOT EXISTS kiosk_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    reg_no TEXT,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_kiosk_events_type ON kiosk_events (event_type);
CREATE INDEX idx_kiosk_events_reg_no ON kiosk_events (reg_no);
