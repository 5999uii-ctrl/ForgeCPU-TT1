# ForgeCPU-TT1

ForgeCPU-TT1 is the first-silicon CPU candidate generated from Forge01-HW for the Tiny Tapeout SKY130 flow.

## Design
- 8-bit accumulator CPU
- 3-bit program counter
- 8 x 8-bit program store
- 4 x 8-bit register file
- 16 opcodes
- LOAD / RUN / INSPECT / HOLD host protocol
- Tiny Tapeout top-level interface
- 10 MHz first-silicon target

## Source of truth
The canonical design is `forge01_source/forgecpu_tt1.f01h`. The checked-in `src/project.v` is generated RTL.

## Verification
This repository contains:
- cocotb RTL tests
- an independent architectural reference model
- static Tiny Tapeout-facing submission checks
- the current TTSKY26d GDS/precheck/gate-level workflow
- a first-silicon bring-up procedure

Physical-silicon completion is not claimed until a fabricated packaged device passes the bring-up tests.
