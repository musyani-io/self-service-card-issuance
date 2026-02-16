# DESIGN NOTES AND ASSUMPTIONS

This document summarizes the component-selection and power-delivery rationale for the EasyEDA schematic.

## Power Subsystem

- 12 V input rated at 15 A: allocate 10 A for motors and 5 A for the Raspberry Pi and logic rails. The ratings include headroom for conversion losses and transient loads.
- Use fuses for protection on the main input and on each regulated rail.
- Reverse-polarity protection is implemented with a P-channel MOSFET. The MOSFET source connects to the fused input, and the drain connects to the protected output rail.
- 12 V to 5 V conversion uses a 10 A synchronous buck regulator to supply the Raspberry Pi and display peripherals with headroom.
- The buck regulator SW node is internally connected to the filter network. Do not add an external low-pass filter; instead, provide a dedicated copper area on the PCB for SW heat spreading.
- Enable (EN) pin requirements: the buck regulator datasheet specifies EN must remain below 3.6 V. Derive EN from the 12 V rail using a divider or level-shift so the applied voltage stays within the limit.
- Connect PGND and AGND at a single point on the PCB. Treat PGND as the high di/dt return and AGND as the quiet reference; use a Kelvin connection at the tie point.
- The 12 V to 5 V buck operates at 1 MHz in forced CCM (FCCM) mode for Raspberry Pi class loads.
