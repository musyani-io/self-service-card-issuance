# hardware_guidelines.md

## Purpose

This document defines the structured tasks and checkpoints for the **hardware design phase** of the Automated Student ID Card Dispensing System.  
The scope of this document ends at **completion and validation of electronic schematics**.  
PCB layout, firmware, and mechanical design are explicitly out of scope at this stage.

---

## Design Principles (Must Be Followed)

- Single power supply architecture (12 V input).
- Clear separation of **logic power** and **actuator power**.
- Deterministic communication between Raspberry Pi and MCU.
- 3.3 V logic compliance for all MCU-connected peripherals.
- Hierarchical schematics (not one flat page).
- Design decisions justified before implementation.

---

## Phase 0 — Pre-Schematic Planning (Completed / In Progress)

### Objectives

- Lock system assumptions before drawing.
- Prevent redesign due to unclear requirements.

### Tasks

- [x] Confirm single power supply strategy (12 V input).
- [x] Decide Raspberry Pi power input method (USB-C vs GPIO 5 V) - USB-C
- [x] Confirm use of Pi Camera for computer vision
- [x] Confirm MCU role as real-time controller only (STM32 - Nucleo)
- [x] Define voltage domains: 12 V, 5 V, 3.3 V.
- [x] Define grounding strategy (star ground).

### Deliverables

- Written design assumptions (notes or README).
- Agreed-upon block diagram (conceptual).

---

## Phase 1 — Power Architecture Design (FIRST SCHEMATIC PHASE)

### Objectives

- Design a stable, safe, and noise-resilient power system.
- Ensure Raspberry Pi stability under load.

### Tasks

- [x] Create POWER schematic sheet.
- [x] Add 12 V DC input connector.
- [x] Add main input protection:
  - Fuse
  - Reverse polarity protection
- [x] Define and label `GND_STAR`.
- [ ] Split power into two branches:
  - Motor/actuator branch
  - Logic branch
- [ ] Add logic branch fuse.
- [ ] Add motor branch fuse.
- [ ] Add bulk capacitors on:
  - 12 V motor rail
  - 5 V logic rail
- [ ] Place 12 V → 5 V buck regulator (rated ≥ Pi peak current).
- [ ] Place 5 V → 3.3 V regulator for logic.
- [ ] Add test points for all power rails.

### Checks Before Proceeding

- Motors are not powered from 5 V or 3.3 V.
- Logic ground and motor ground meet only at `GND_STAR`.
- All rails are clearly named and labeled.

### Deliverables

- POWER schematic (PDF export).
- Annotated notes explaining power choices.

---

## Phase 2 — Raspberry Pi Interface Schematic

### Objectives

- Define all electrical connections to the Raspberry Pi.
- Avoid misuse of GPIO pins.

### Tasks

- [ ] Create RPI_INTERFACES schematic sheet.
- [ ] Represent Raspberry Pi using a 40-pin GPIO header symbol.
- [ ] Connect:
  - 5 V input
  - GND
- [ ] Expose only required GPIOs:
  - SPI (SCK, MOSI, MISO, CS)
  - Optional interrupt line from MCU
- [ ] Represent Pi Camera as CSI interface (no separate power).
- [ ] Represent USB ports symbolically (no GPIO wiring).

### Checks Before Proceeding

- No peripheral draws power directly from Pi GPIO pins.
- No 5 V signals enter Pi GPIO.
- Pi GPIO logic is treated as 3.3 V only.

### Deliverables

- Raspberry Pi interface schematic (PDF).

---

## Phase 3 — MCU (STM32 or Alternative) Interface Schematic

### Objectives

- Define MCU power and I/O clearly.
- Prepare for clean actuator and sensor integration later.

### Tasks

- [ ] Create STM32_INTERFACES schematic sheet.
- [ ] Represent MCU board (e.g., Nucleo) via headers.
- [ ] Connect:
  - 3.3 V logic power
  - GND
- [ ] Expose communication pins:
  - SPI (slave mode)
  - Optional UART for debugging
- [ ] Expose GPIOs for:
  - Motor control
  - Sensors
- [ ] Add decoupling (symbolic if using dev board).

### Checks Before Proceeding

- All MCU GPIOs operate at 3.3 V.
- No sensor powered at 5 V connects directly to MCU GPIO.

### Deliverables

- MCU interface schematic (PDF).

---

## Phase 4 — Pi ↔ MCU Communication Design

### Objectives

- Ensure fast, reliable, deterministic communication.

### Tasks

- [ ] Create COMMS schematic section or sheet.
- [ ] Implement SPI bus:
  - SCK
  - MOSI
  - MISO
  - CS
- [ ] Add series resistors on SPI lines (22–47 Ω).
- [ ] Add optional MCU → Pi interrupt line.
- [ ] Label signal direction clearly.

### Checks Before Proceeding

- Only one SPI master (Raspberry Pi).
- No voltage level mismatch.
- All communication signals reference logic ground.

### Deliverables

- Communication schematic (PDF).

---

## Phase 5 — Peripheral Power & Logic Compliance Review

### Objectives

- Prevent GPIO damage and logic mismatch.

### Tasks

- [ ] Verify all sensors connected to MCU are powered at 3.3 V.
- [ ] Confirm pull-ups reference correct voltage rail.
- [ ] Flag any 5 V peripherals requiring level shifting.
- [ ] Document any exceptions explicitly.

### Deliverables

- Peripheral compliance checklist.
- Notes for later motor/sensor integration.

---

## Phase 6 — Schematic Finalization & Review

### Objectives

- Lock schematics before PCB or firmware work begins.

### Tasks

- [ ] Cross-check all net names and power rails.
- [ ] Ensure no unconnected power pins.
- [ ] Ensure all grounds are intentional.
- [ ] Export final PDFs:
  - POWER
  - RPI_INTERFACES
  - MCU_INTERFACES
  - COMMS
- [ ] Generate preliminary BOM from schematic.

### Final Deliverables

- Complete schematic set (PDF).
- EasyEDA Pro project file.
- Preliminary BOM.
- Design notes ready for supervisor review.

---

## Exit Criteria (Schematics Phase Complete)

Schematics are considered complete when:

- Power integrity is defensible.
- All interfaces are electrically correct.
- No assumptions remain undocumented.
- Supervisor feedback is addressed.

Only after this point may PCB layout begin.
