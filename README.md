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

## Project Structure

```bash
computer_vision/          # CV module: barcode detection & verification
  ├── image_capture.py   # Camera interface
  ├── image_utils.py     # Preprocessing functions
  ├── barcode_reader.py  # Barcode detection & decoding
  ├── retry_handler.py   # Retry logic with backoff
  ├── quality_validator.py
  ├── metrics.py
  ├── exceptions.py
  ├── logging_config.py
  └── tests/

raspberry-pi/             # Main application & hardware control
  ├── main.py
  ├── core/              # Workflows, authentication, card manager
  ├── hardware/          # Mock & real hardware interfaces
  ├── database/          # Models, schema, transaction logging
  ├── config/            # Settings & hardware configuration
  └── tests/

stm32-firmware/           # Real-time control firmware (STM32)

docs/                     # Implementation guides & plans
```

## Key Features

- **OTP Authentication**: SMS-based one-time passwords for student identity verification
- **Computer Vision**: Barcode scanning with automatic preprocessing and retry logic
- **Audit Trail**: Complete transaction logging with timestamps and user actions
- **Safety Enforcement**: Mechanical limits, jam detection, and error recovery
- **Mock Hardware**: Full testing without physical hardware

## Progress

### Computer Vision Module

**Completion:** 15/168 tasks (~8.9%)

#### Completed Phases

- ✅ Phase 1.3: Development environment setup
- ✅ Phase 3.1: Basic image preprocessing

#### In Progress

- 🔄 Phase 1: Environment Setup & Hardware Preparation
- 🔄 Phase 2: Image Capture
- 🔄 Phase 3: Image Preprocessing
- 🔄 Phase 4: Barcode Detection & Decoding

#### Roadmap

1. **Phase 1-2** (Weeks 1): Setup & basic camera capture
2. **Phase 3-4** (Week 2): Preprocessing & barcode reading
3. **Phase 5-6** (Week 3): Error handling & system integration
4. **Phase 7-8** (Week 4): Calibration & documentation

See [cv_guideline.md](computer_vision/cv_guideline.md) for detailed task breakdown.

### Raspberry Pi Module

**Completion:** 0% (No implementation guidelines yet)

- Hardware interfaces defined
- Database schema in planning

### STM32 Firmware Module

**Completion:** 0% (No implementation guidelines yet)

- Firmware architecture in planning
- Hardware control protocol defined

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) file for full details.

## Status

**Developmental**: API and architecture subject to change. Not production-ready.
