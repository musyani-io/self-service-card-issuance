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
- `VIN_12_PROT` — Protected 12 V after fuse & reverse polarity
- `V12_LOGIC`
- `V12_MOTOR`
- `V5_PI` — 5.1 V rail for Raspberry Pi
- `V3V3_LOGIC` — 3.3 V rail for MCU and sensors
- `VBUS_OUT` — USB-C output rail
- `GND_LOGIC`
- `GND_MOTOR`
- `GND_STAR` — single-point ground reference (implemented via net-tie)

---

# Mandatory Design Principles

1. Single 12 V supply input.
2. Clear separation between:
   - Logic power
   - Actuator/motor power
3. Raspberry Pi powered from regulated 5.1 V rail via USB-C PD source.
4. MCU powered from regulated 3.3 V rail only.
5. No GPIO ever exposed to 5 V unless explicitly level shifted.
6. Deterministic communication (SPI preferred).
7. Hierarchical schematics — no single flat-page design.
8. All control pins must be intentionally defined.
9. All power rails must include local decoupling.
10. All external connectors must include protection.
11. All design decisions must be justified before implementation.

---

# PHASE 0 — Project Setup (KiCad Structure)

## Objectives

Establish a clean schematic hierarchy and naming convention.

## Tasks

- [x] Create KiCad project.
- [x] Create hierarchical sheets:
  - `POWER.sch`
  - `BUCK_5V.sch`
  - `BUCK_3V3.sch`
  - `USB_C_PD_SOURCE.sch`
  - `RPI_INTERFACES.sch`
  - `MCU_INTERFACES.sch`
  - `COMMS.sch`
  - `PERIPHERALS.sch` (optional)
- [ ] Define standardized global net labels.
- [ ] Define net classes (high-current vs logic).
- [ ] Define ground nets (`GND_LOGIC`, `GND_MOTOR`).
- [ ] Plan star-ground implementation using net-tie.
- [ ] Place test-point symbols library for later use.

## Execution Notes

- Do not place components until nets are named.
- Do not merge grounds prematurely.
- All hierarchical sheet pins must be explicitly named.

---

# PHASE 1 — Power Architecture Design (POWER.sch)

This is the most critical phase.

---

## Section 1 — 12 V Input & Protection

### Objectives

Protect the system from wiring errors and faults.

### Tasks

- [ ] Add 12 V input connector (rated ≥ 20 A).
- [ ] Add main fuse (slow-blow, rated above steady-state total system current).
- [ ] Add reverse polarity protection:
  - Preferred: P-channel MOSFET ideal-diode configuration
  - Alternative: Schottky diode (only if voltage drop acceptable)
- [ ] Define protected input net (`VIN_12_PROT`).
- [ ] Add bulk capacitor immediately after protection.
- [ ] Add TVS diode on 12 V input (optional but recommended).
- [ ] Define `GND_LOGIC` and `GND_MOTOR`.

### Checks

- Protection precedes rail branching.
- Reverse polarity solution voltage drop < acceptable margin.
- 12 V entry decoupled locally.

---

## Section 2 — Rail Separation

### Logic Branch

- [ ] Add dedicated fuse (5–10 A range depending on design).
- [ ] Define `V12_LOGIC`.
- [ ] Add bulk capacitor (≥470 µF recommended).
- [ ] Add ceramic decoupling.
- [ ] Add test point.

### Motor Branch

- [ ] Add dedicated fuse (≥10 A blade type).
- [ ] Define `V12_MOTOR`.
- [ ] Add bulk capacitor sized for motor transient demand.
- [ ] Add test point.

### Ground Strategy

- [ ] Keep `GND_LOGIC` and `GND_MOTOR` separated.
- [ ] Place net-tie symbol for star point.
- [ ] Ensure only one connection exists between grounds.

### Checks

- No direct wire short between grounds.
- Motor branch cannot inject noise directly into logic rail.

---

## Section 3 — 12 V → 5.1 V Regulator (Raspberry Pi Rail)

### Objectives

Provide stable 5.1 V under peak load conditions (target ≥ 5 A continuous).

### Tasks

- [x] Select synchronous buck topology.
- [x] Ensure regulator supports:
  - ≥12 V input
  - ≥8 A peak capability
  - Integrated or external MOSFET solution
- [ ] Add input capacitors:
  - 100 nF ceramic
  - ≥2×22 µF ceramics
- [ ] Add inductor sized for:
  - Saturation current ≥ 1.5× peak load
- [ ] Add output capacitors:
  - ≥2×22 µF ceramics
  - Bulk electrolytic for transient response
- [ ] Configure feedback for 5.1 V output.
- [ ] Configure EN pin (always-on or controlled).
- [ ] Define `V5_PI`.
- [ ] Add test point.

### Checks

- Switching node clearly identified.
- Output ripple acceptable.
- No motor loads connected to this rail.

---

## Section 4 — 12 V → 3.3 V Regulator (MCU Rail)

### Objectives

Provide clean 3.3 V with noise margin.

### Tasks

- [x] Select synchronous buck topology (preferred).
- [x] Input decoupling placed near regulator.
- [x] Inductor sized appropriately.
- [x] Output capacitors placed.
- [x] Configure feedback divider.
- [x] Configure EN (always-on).
- [x] Define `V3V3_LOGIC`.
- [x] Add test point.

### Checks

- 3.3 V independent of 5 V rail.
- Feedback referenced to `GND_LOGIC`.
- Adequate current margin.

---

# PHASE 1.5 — USB-C 5V / 5A PD Source Implementation

## Objectives

Provide compliant USB-C 5 V only, 5 A capable source for Raspberry Pi.

---

## Section 1 — USB-C Connector

- [ ] Place USB-C receptacle.
- [ ] Connect:
  - All VBUS pins → `VBUS_OUT`
  - All GND pins → `GND_LOGIC`
  - CC1/CC2 defined as separate nets
- [ ] Add ESD protection on CC1 and CC2.
- [ ] Add TVS diode on VBUS_OUT.

---

## Section 2 — Power Path Switch

- [ ] Implement controlled high-side power switch:
  - Back-to-back N-MOSFETs OR
  - High-current load switch IC
- [ ] Ensure continuous current rating ≥ 5 A.
- [ ] Ensure reverse current blocking.
- [ ] Add local decoupling at VIN_5V side.

---

## Section 3 — PD Source Controller

- [ ] Select PD controller supporting:
  - Source mode
  - 5 V only configuration
  - 5 A advertisement
- [ ] Connect CC1/CC2 to controller.
- [ ] Connect gate/enable to power switch.
- [ ] Connect VBUS sense.
- [ ] Provide controller supply (3.3 V or 5 V as required).
- [ ] Implement configuration (strap or EEPROM).
- [ ] Implement discharge path if required.

---

## Section 4 — Validation

- [ ] Ensure VBUS is not permanently tied to V5_PI.
- [ ] Ensure attach detection required before enabling VBUS.
- [ ] Ensure short-circuit protection exists.
- [ ] Confirm cable hot-plug behavior considered.

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

## Additional Checks

- [ ] Verify USB-C power path integrity.
- [ ] Verify star-ground implementation consistent.
- [ ] Verify high-current nets assigned proper net class.
- [ ] Verify no floating EN pins.
- [ ] Verify no control pins left undefined.

---

# Exit Criteria

Schematics are complete when:

- Power system is technically defensible.
- USB-C behaves as controlled 5V/5A source.
- Voltage domains are cleanly separated.
- Protection strategy implemented.
- ERC clean or justified.
- Design ready for supervisor review.

Only after this stage may PCB layout begin.
