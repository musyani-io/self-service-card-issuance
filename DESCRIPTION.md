# Automated Self-Service Student ID Card Issuance System

## Overview

This project implements a prototype **Automated Self-Service Student ID Card Issuance System** designed to securely distribute **pre-printed student ID cards** in a university environment. The system eliminates long queues, limited working hours, and manual sorting by enabling **on-demand, 24/7 card retrieval** through a secure, auditable, and electromechanically controlled kiosk.

The system focuses strictly on **card distribution**, not card printing or identity creation.

---

## Problem Statement

In many universities, including the University of Dar es Salaam, student ID cards are issued through a largely manual process:

- Cards are pre-printed and later distributed at college offices
- Students wait days to weeks before collection
- Distribution is constrained to working hours
- Staff must manually sort and handle large volumes of cards
- The process is prone to inefficiency, congestion, and human error

The bottleneck is **secure distribution**, not printing.

---

## Project Objective

### Main Objective

To design and implement an **automated, secure, and reliable self-service system** for issuing pre-printed student ID cards with full transaction logging and minimal human intervention.

### Specific Objectives

- Implement a deterministic actuator control system capable of selecting and dispensing a single card
- Implement secure student authentication using SMS-based One-Time Passwords (OTP)
- Implement computer vision for card identification and verification
- Maintain a complete audit trail of all transactions
- Enforce security policies for invalid attempts and physical tampering
- Evaluate system performance using measurable operational metrics

---

## System Scope and Limitations

### Included

- Secure dispensing of **pre-printed** ID cards
- Mechanical card transport, stopping, and storage
- OTP-based authentication
- Computer vision verification
- Local (mock) database for testing
- Audit logging and fault reporting

### Excluded

- On-device PVC card printing
- Payment or billing systems
- Mobile applications
- Direct access to live university databases (unless authorized)

---

## System Architecture

The system uses a **dual-controller architecture** to separate high-level decision logic from real-time mechanical control.

### High-Level Controller (Raspberry Pi 5)

Responsibilities:

- User interface (display, keypad, scanner input)
- SMS OTP generation and verification
- Database access and transaction logging
- Computer vision processing
- Security policy enforcement
- Issuing structured commands to the real-time controller

This controller handles **logic, authentication, and traceability**.

### Low-Level Controller (STM32)

Responsibilities:

- Real-time motor and actuator control
- Sensor acquisition (optical sensors, limit switches, jam detection)
- Deterministic execution of card transport and dispensing
- Mechanical safety enforcement
- Status and fault reporting to the high-level controller

This controller handles **physical determinism and safety**.

### Communication

- Protocol: SPI
- Logic level: 3.3 V
- Direction: Command–status exchange between Raspberry Pi and STM32

---

## Card Handling and Transport Concept

- Cards are **pre-printed** and manually loaded by authorized staff
- Each card contains a **printed student ID** used as a unique identifier (OCR)
- Cards are stored in indexed compartments
- A roller-based transport mechanism:
  - Accepts cards from the input slot
  - Moves cards to a camera inspection point
  - Stops cards at a repeatable reference position
  - Routes cards to storage or rejects them back to the user

All motion is **mechanically constrained** to ensure alignment and repeatability.

---

## Functional Workflow

### 1. Preload and Mapping Phase (Staff Operation)

- Staff loads pre-printed cards into the machine
- Each card is scanned using a camera
- Card student ID (OCR) is mapped to a storage index and student record
- Mapping is stored in the database

### 2. Notification Phase

- Once cards are available, the system sends an SMS notification
- Each message includes an OTP valid for a single retrieval attempt

### 3. Retrieval Phase (Student Operation)

1. Student inserts or scans their expired ID card
2. Student details are displayed on the screen
3. Student enters the OTP received via SMS
4. System verifies identity and OTP
5. High-level controller authorizes dispensing
6. Low-level controller retrieves and ejects the correct card
7. Transaction is logged for auditing

### 4. Rejection and Error Handling

- If verification or vision checks fail:
  - Card can be safely rejected back to the user
- If mechanical or security faults occur:
  - System halts and notifies the administrator

---

## Security Model

### Logical Security

- SMS-based OTP authentication
- Limited retry attempts
- Temporary lockout after repeated failures
- Database-backed audit logging

### Physical Security

- Tamper detection sensors
- Jam and stall detection
- Motor torque limiting
- Manual administrator reset for recovery

The system prioritizes **human safety over mechanical force**.

---

## Performance Evaluation Metrics

The prototype is evaluated using:

- Authentication success rate
- Average card retrieval time
- Dispense accuracy (correct card delivered)
- Fault detection and recovery effectiveness
- System uptime and reliability

---

## Key Engineering Contributions

- Application of vending-machine principles to sensitive identity distribution
- Correct separation of real-time and non-real-time system responsibilities
- Secure, auditable automation for institutional ID management
- Mechanically enforced precision to reduce software complexity

---

## Intended Use

This prototype is intended for:

- Academic evaluation
- Demonstration of embedded systems integration
- Exploration of secure automated kiosks in institutional environments

It is **not** intended for direct deployment without further industrial hardening.

---
