import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

# Gate-level SKY130 simulation uses unit delays through multiple cells.
# Sample well after the active edge so both RTL and GL tests observe settled state.
SETTLE_NS = 20

async def settle():
    await Timer(SETTLE_NS, unit="ns")

async def load_byte(dut, addr, data):
    dut.ui_in.value = addr & 0x7
    dut.uio_in.value = data
    await ClockCycles(dut.clk, 1)
    await settle()

async def reset_cpu(dut):
    dut.rst_n.value = 0
    dut.ui_in.value = 0xC0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    await settle()
    dut.rst_n.value = 1
    await settle()

async def run_cycles(dut, n):
    dut.ui_in.value = 0x40
    await ClockCycles(dut.clk, n)
    await settle()

async def inspect(dut, value):
    dut.ui_in.value = value
    await settle()
    return int(dut.uo_out.value)

@cocotb.test()
async def test_forgecpu_tt1(dut):
    cocotb.start_soon(Clock(dut.clk, 100, unit="ns").start())
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await settle()

    # Program A: exercise ALU, STORE/LOAD, DEC, HALT.
    await reset_cpu(dut)
    for a, b in enumerate([0x13,0x24,0x42,0xD0,0x70,0xC0,0x80,0xF0]):
        await load_byte(dut, a, b)
    await run_cycles(dut, 8)
    assert int(dut.uo_out.value) == 10
    assert await inspect(dut, 0x83) == 1   # HALT
    assert await inspect(dut, 0x81) == 7   # PC
    assert await inspect(dut, 0x82) == 10  # R0

    # Program B: taken JZ plus STORE to R1.
    await reset_cpu(dut)
    for a, b in enumerate([0x10,0xA4,0x19,0xF0,0x15,0x23,0x71,0xF0]):
        await load_byte(dut, a, b)
    await run_cycles(dut, 6)
    assert int(dut.uo_out.value) == 8
    assert await inspect(dut, 0x86) == 8   # R1
    assert await inspect(dut, 0x83) == 1   # HALT

    # ena=0 must prevent a LOAD-mode program write.
    await reset_cpu(dut)
    dut.ena.value = 1
    await load_byte(dut, 0, 0x10)
    dut.ena.value = 0
    await load_byte(dut, 0, 0x15)
    dut.ena.value = 1
    await load_byte(dut, 1, 0xF0)
    await run_cycles(dut, 1)
    assert int(dut.uo_out.value) == 0

    # ena=0 must also prevent CPU execution.
    await reset_cpu(dut)
    dut.ena.value = 1
    await load_byte(dut, 0, 0x15)
    await load_byte(dut, 1, 0xF0)
    dut.ena.value = 0
    dut.ui_in.value = 0x40
    await ClockCycles(dut.clk, 1)
    await settle()
    assert await inspect(dut, 0x81) == 0  # PC unchanged
    assert await inspect(dut, 0x80) == 0  # ACC unchanged
    dut.ena.value = 1
    await run_cycles(dut, 1)
    assert int(dut.uo_out.value) == 5

    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0
