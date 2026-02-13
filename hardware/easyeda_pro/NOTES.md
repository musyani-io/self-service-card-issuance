# DESIGN NOTES AND ASSUMPTIONS

This document summarizes the component and power-delivery rationale for the EasyEDA schematic.

## Power Subsystem

- 12 V input rated at 15 A: allocate 10 A for motors and 5 A for the Raspberry Pi and logic rails. The ratings include headroom for conversion losses and transient loads.
- Use fuses for protection on the main input and on each regulated rail.
- Reverse-polarity protection is implemented with a P-channel MOSFET. The MOSFET source connects to the fused input, and the drain connects to the protected output rail.
