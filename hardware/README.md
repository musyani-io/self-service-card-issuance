# Hardware Design and Integration

This directory contains the electrical design, PCB layout, and mechanical specifications for the self-service card issuance kiosk controller board, designed using KiCAD.

## Design Overview

The hardware implements a dual-controller architecture:

- **Raspberry Pi 5**: High-level application control, UI, vision processing, and system logging
- **STM32 Microcontroller**: Real-time actuator control, sensor acquisition, and safety interlocks
- **SPI Communication**: 3.3V differential signaling for deterministic inter-controller messaging

## Design Files

KiCAD project files are located in [kicad/](kicad/) with four independent circuit modules:

- **buck_3V3.kicad_pro**: 12V → 3.3V buck regulator for logic and STM32 supply
- **buck_5V1.kicad_pro**: 12V → 5V synchronous buck regulator (10 A) for Raspberry Pi and peripherals
- **motor_driver.kicad_pro**: High-side MOSFET drivers and PWM control for DC motor actuation
- **reverse_polarity.kicad_pro**: Input reverse-polarity protection circuit using P-channel MOSFET

Each project includes schematic (.kicad_sch), PCB layout (.kicad_pcb), and project configuration files.

## Schematic Exports

Generated schematics are exported as PDFs in the [schematics/](schematics/) directory for documentation and reference.

## PCB Layout

PCB layout files and manufacturing exports are available in [pcb/](pcb/):

- Multi-layer stackup optimized for power distribution and thermal management
- Dedicated copper area under buck regulator SW nodes for heat spreading
- Ground plane separation (PGND/AGND) with single-point Kelvin connection

## Simulations

Circuit simulations and verification are performed in [simulations/](simulations/) using Proteus (.pdsprj files) for behavioral validation of power stages and driver circuits.

## 3D Models and Renders

3D visualizations are provided in [3d/](3d/):

- Component placement and thermal analysis renderings
- PCB assembly reference

## Bill of Materials

Component lists and sourcing information:

- [bom/motor_driver.csv](bom/motor_driver.csv): Motor driver stage components

## Component Datasheets

Reference datasheets for key active components are provided in [datasheets/](datasheets/):

- Buck regulator specifications and timing parameters
- Motor driver absolute maximum ratings and thermal considerations
- Reverse-polarity MOSFET characteristics

## Design Constraints and Specifications

- **Input voltage**: 12 V nominal (fused at 10 A)
- **Output rails**: 5 V @ 8 A (Pi/display), 3.3 V @ 3 A (logic/STM32)
- **Operating mode**: 12V → 5V buck in 1 MHz forced CCM for Raspberry Pi loads
- **Safety**: Dual fusing, reverse-polarity protection, limit switch monitoring on STM32
