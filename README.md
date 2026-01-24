# Self-Service Card Issuance System

Automated, secure, 24/7 student ID card distribution kiosk for universities.

## Overview

This project implements a **dual-controller architecture** for secure, auditable self-service distribution of pre-printed student ID cards:

- **Raspberry Pi 5**: High-level logic, authentication (OTP-based), computer vision, database access
- **STM32**: Real-time motor/actuator control, sensor acquisition, mechanical safety

## Architecture

```bash
┌─────────────────────────────────────────┐
│   Raspberry Pi 5 (High-Level Control)   │
│  • User Interface & Display             │
│  • SMS OTP Authentication               │
│  • Computer Vision (Barcode Scanning)   │
│  • Database & Audit Logging             │
└────────────────────┬────────────────────┘
                     │ SPI (3.3V)
                     │
┌────────────────────▼────────────────────┐
│    STM32 (Low-Level Control)            │
│  • Motor & Actuator Control             │
│  • Sensor I/O (Optical, Limit Switches) │
│  • Deterministic Card Transport         │
│  • Jam Detection & Safety               │
└─────────────────────────────────────────┘
```

## Key Features

- **OTP Authentication**: SMS-based one-time passwords for student identity verification
- **Computer Vision**: Barcode scanning with automatic preprocessing and retry logic
- **Audit Trail**: Complete transaction logging with timestamps and user actions
- **Safety Enforcement**: Mechanical limits, jam detection, and error recovery
- **Mock Hardware**: Full testing without physical hardware
