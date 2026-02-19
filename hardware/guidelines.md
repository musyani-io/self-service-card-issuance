# hardware_guidelines.md

## Purpose

This document defines the structured workflow and technical checkpoints for the **schematic design phase** of the Automated Student ID Card Dispensing System.

This version is intentionally **component-agnostic**.  
Specific ICs, regulators, and drivers will be selected during the design process based on validated requirements.

Scope ends at:

- Fully validated hierarchical schematics
- Defensible power architecture
- Electrically correct interfaces

PCB layout, firmware, and mechanical integration are explicitly out of scope.

---

# Core System Architecture

## Voltage Domains (Planned)

- `VIN_12` — Raw 12 V input
- `V12_LOGIC`
- `V12_MOTOR`
- `V5_PI` — 5 V rail for Raspberry Pi
- `V3V3_LOGIC` — 3.3 V rail for MCU and sensors
- `GND_LOGIC`
- `GND_MOTOR`
- `GND_STAR` — single-point ground reference

---

# Mandatory Design Principles

1. Single 12 V supply input.
2. Clear separation between:
   - Logic power
   - Actuator/motor power
3. Raspberry Pi powered from regulated 5 V rail only.
4. MCU powered from regulated 3.3 V rail only.
5. No GPIO ever exposed to 5 V unless explicitly level shifted.
6. Deterministic communication (SPI preferred).
7. Hierarchical schematics — no single flat-page design.
8. All control pins must be intentionally defined.
9. All power rails must include local decoupling.
10. All design decisions must be justified before implementation.

---

# PHASE 0 — Project Setup (KiCad Structure)

## Objectives

Establish a clean schematic hierarchy and naming convention.

## Tasks

- [x] Create KiCad project.
- [x] Create hierarchical sheets:
  - `POWER.sch`
  - `RPI_INTERFACES.sch`
  - `MCU_INTERFACES.sch`
  - `COMMS.sch`
  - `PERIPHERALS.sch` (optional, later)
- [ ] Define standardized global net labels:
  - `VIN_12`
  - `V12_LOGIC`
  - `V12_MOTOR`
  - `V5_PI`
  - `V3V3_LOGIC`
  - `GND_LOGIC`
  - `GND_MOTOR`
- [ ] Plan star-ground strategy (implemented using net-tie in PCB phase).

## Exit Criteria

- No schematic content yet.
- Clean structure.
- Consistent net naming.

---

# PHASE 1 — Power Architecture Design (POWER.sch)

This is the most critical phase.

---

## Section 1 — 12 V Input & Protection

### Objectives

Protect the system from wiring errors and faults.

### Tasks

- [ ] Add 12 V input connector.
- [ ] Add main fuse (rated above expected steady-state current).
- [ ] Add reverse polarity protection (method to be selected later).
- [ ] Define protected input net (`VIN_12_PROT`).
- [ ] Define `GND_LOGIC` and `GND_MOTOR`.

### Checks

- Protection precedes branching.
- Reverse polarity solution does not introduce excessive voltage drop.
- Ground reference defined clearly.

---

## Section 2 — Rail Separation

### Logic Branch

- [ ] Add dedicated fuse.
- [ ] Define `V12_LOGIC`.
- [ ] Add bulk capacitor (energy reservoir).
- [ ] Add test point.

### Motor Branch

- [ ] Add dedicated fuse.
- [ ] Define `V12_MOTOR`.
- [ ] Add bulk capacitor.
- [ ] Add test point.

### Checks

- No direct cross-connection between logic and motor rails.
- Grounds meet only at defined star point.

---

## Section 3 — 12 V → 5 V Regulator (Raspberry Pi Rail)

### Objectives

Provide stable 5 V under peak load conditions.

### Tasks

- [ ] Select regulator topology (buck converter expected).
- [ ] Verify:
  - Input voltage range ≥ 12 V
  - Output current rating ≥ Pi peak load
  - Protection features (OCP, OTP, UVLO)
- [ ] Add required:
  - Input capacitors (local ceramics mandatory)
  - Output capacitors
  - Feedback network (if adjustable)
  - Enable configuration
- [ ] Define `V5_PI`.
- [ ] Add test point.

### Checks

- No motor loads powered from 5 V rail.
- Regulator control pins not left floating.
- Output current rating has margin.

---

## Section 4 — 12 V → 3.3 V Regulator (MCU Rail)

### Objectives

Provide clean, noise-resistant 3.3 V for MCU and sensors.

### Tasks

- [ ] Select regulator topology (buck preferred for efficiency).
- [ ] Verify:
  - Input range supports 12 V
  - Output current ≥ MCU + sensor load
- [ ] Add:
  - Input capacitors (local)
  - Inductor (if required)
  - Output capacitors
  - Feedback divider
  - Enable configuration (always-on)
- [ ] Define `V3V3_LOGIC`.
- [ ] Add test point.

### Checks

- 3.3 V rail independent of 5 V rail.
- Feedback network referenced to correct ground.
- Output ripple acceptable for MCU operation.

---

# PHASE 2 — Raspberry Pi Interface

## Objectives

Safely interface Raspberry Pi.

### Tasks

- [ ] Represent Pi using 40-pin header.
- [ ] Connect:
  - `V5_PI`
  - `GND_LOGIC`
- [ ] Expose required SPI pins.
- [ ] Add series resistors (22–47 Ω) on high-speed lines.
- [ ] Add optional interrupt line.

### Checks

- No GPIO exposed to 5 V.
- Only one SPI master (Pi).
- No external loads powered from GPIO pins.

---

# PHASE 3 — MCU Interface

## Objectives

Define MCU electrical boundary clearly.

### Tasks

- [ ] Represent MCU board or chip.
- [ ] Connect `V3V3_LOGIC`.
- [ ] Connect `GND_LOGIC`.
- [ ] Expose SPI (slave mode).
- [ ] Expose GPIO for:
  - Motor drivers
  - Sensors
- [ ] Add symbolic decoupling (or explicit if bare MCU).

### Checks

- All MCU I/O at 3.3 V.
- No 5 V peripherals directly connected.

---

# PHASE 4 — Communication Architecture

## Objectives

Ensure deterministic and robust data exchange.

### Tasks

- [ ] Implement SPI bus connections.
- [ ] Add series resistors.
- [ ] Label direction clearly.
- [ ] Confirm ground reference consistency.

### Checks

- Single SPI master.
- No floating communication lines.

---

# PHASE 5 — Peripheral Compliance Review

## Objectives

Prevent voltage domain violations.

### Tasks

- [ ] Confirm all sensors operate at 3.3 V.
- [ ] Identify required level shifting.
- [ ] Ensure motor control signals go through drivers.
- [ ] Confirm no direct exposure of logic to 12 V.

---

# PHASE 6 — Schematic Finalization

## Objectives

Lock schematic integrity before PCB layout.

### Tasks

- [ ] Run ERC and resolve all warnings.
- [ ] Verify all control pins defined.
- [ ] Confirm all grounds intentional.
- [ ] Ensure each power rail has test point.
- [ ] Export schematic PDFs.
- [ ] Generate preliminary BOM (component-agnostic placeholders allowed).

---

# Exit Criteria

Schematics are complete when:

- Power system is technically defensible.
- Voltage domains are cleanly separated.
- Interfaces are electrically safe.
- No undocumented assumptions remain.
- Design is supervisor-ready.

Only after this stage may PCB layout begin.
