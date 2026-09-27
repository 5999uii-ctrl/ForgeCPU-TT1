# ForgeCPU-TT1 first-silicon bring-up

1. Start with the Tiny Tapeout carrier/controller at a conservative clock.
2. Assert reset across a rising edge, release reset, then inspect ACC/PC/HALT = 0.
3. Load Program A in LOAD mode: `13 24 42 D0 70 C0 80 F0`.
4. Run 8 clocks. Expected ACC=10, PC=7, R0=10, HALT=1.
5. Reset and load Program B: `10 A4 19 F0 15 23 71 F0`.
6. Run 6 clocks. Expected ACC=8, PC=7, R1=8, HALT=1.
7. Verify `ena=0` prevents both program-memory writes and CPU execution.
8. Only after functional checks pass, sweep frequency toward the signed-off target.

REAL SILICON COMPLETE requires these functional gates on a physical packaged device.
