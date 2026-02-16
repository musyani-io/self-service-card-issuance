# Self-Service Card Issuance System

Automated, secure, 24/7 student ID card distribution kiosk with a dual-controller architecture and full auditability.

## Overview

This system dispenses pre-printed student ID cards after identity verification. It is designed for unattended operation with deterministic control, mechanical safety, and a complete audit trail.

## System Architecture

Two controllers split responsibilities:

- **Raspberry Pi 5 (High-Level Control)**
  - User interface and session management
  - OTP-based authentication and policy enforcement
  - Computer vision pipeline for OCR/verification
  - Database access and audit logging

- **STM32 (Low-Level Control)**
  - Motor/actuator control and transport timing
  - Sensor acquisition (optical, limit switches, etc.)
  - Jam detection and recovery state machine
  - Hardware safety interlocks

Communication occurs over a 3.3V SPI link with a message protocol and acknowledgements to ensure safe, deterministic execution.

## Key Features

- **OTP Authentication**: SMS-based verification with configurable timeouts and retries
- **Computer Vision**: OCR-driven ID extraction with preprocessing and failure handling
- **Audit Trail**: Immutable transaction logs with timestamps and device context
- **Safety Enforcement**: Jam detection, limit checks, and fault isolation
- **Offline Tolerance**: Local caching for continued operation during network issues
- **Mock Hardware**: Back-end testing without physical hardware

## Repository Structure

- [DESCRIPTION.md](DESCRIPTION.md): Short project description and scope
- [backend/](backend/): Raspberry Pi application (auth, dispense flow, logging, DB access, communications)
- [computer_vision/](computer_vision/): CV pipeline for detection, OCR, and verification
- [hardware/](hardware/): Schematics, PCB layouts, BOMs, and EasyEDA project files
- [docs/](docs/): Research, system guidelines, and internal documentation
- [usage/](usage/): Minimal usage examples and entry points

## Data Flow (High Level)

1. User initiates session on the kiosk UI.
2. OTP is issued and verified.
3. The CV pipeline validates the card identity.
4. The Pi sends a dispense command to STM32.
5. STM32 executes the transport state machine and reports status.
6. Results and telemetry are logged.

## Hardware Integration

Hardware artifacts are organized under [hardware/](hardware/) and include:

- Schematics and PCB layouts
- BOMs and component datasheets
- EasyEDA project files

## Development Notes

- The Pi side is responsible for policies, logging, and vision.
- The STM32 side is responsible for deterministic actuation and safety.
- All dispense actions must be logged with outcome codes.

## License

See [LICENSE](LICENSE).
