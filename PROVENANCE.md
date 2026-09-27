# ForgeCPU-TT1 provenance

Canonical design source: `forge01_source/forgecpu_tt1.f01h`.

The checked-in `src/project.v` is generated from Forge01-HW source rather than being the canonical hand-written design.

Local-closure provenance before GitHub ASIC hardening:
- Forge01 native compiler fixed point: Stage1 == Stage2 == Stage3.
- No C/C++ implementation source in the Forge01 release.
- RTL and metadata passed the local submission/static checks.

External proof gates are GitHub RTL simulation, Tiny Tapeout GDS/LibreLane hardening, precheck, gate-level simulation, and eventually physical first-silicon bring-up.
