# ForgeCPU-TT1

ForgeCPU-TT1 is the first ASIC tapeout candidate generated from Forge01-HW. It is an 8-bit accumulator CPU with an 8-byte program memory, four 8-bit general-purpose registers, a 3-bit PC, ALU, decoder, branch control and HALT state.

The host interface uses `ui_in[7:6]` as a mode selector:
- `00`: program-load mode. `ui_in[2:0]` is the program address and `uio_in[7:0]` is the instruction byte.
- `01`: run mode. One instruction per rising clock edge while `ena=1`.
- `10`: inspect mode.
- `11`: hold mode.

`uio` is input-only in this design (`uio_oe=0`).

Instruction byte = opcode[7:4] | arg[3:0].
Opcodes: NOP, LDI, ADDI, SUBI, XORI, ANDI, ORI, STORE, LOAD, JMP, JZ, INC, DEC, SHL, SHR, HALT.

To test: reset, load 8 program bytes in LOAD mode, switch to RUN, then use INSPECT to read ACC/PC/register/HALT state.
