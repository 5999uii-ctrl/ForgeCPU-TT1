import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

async def load_byte(dut, addr, data):
    dut.ui_in.value = addr & 0x7
    dut.uio_in.value = data
    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")

async def reset_cpu(dut):
    dut.rst_n.value = 0
    dut.ui_in.value = 0xC0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")
    dut.rst_n.value = 1

async def run_cycles(dut, n):
    dut.ui_in.value = 0x40
    await ClockCycles(dut.clk, n)
    await Timer(1, unit="ns")

@cocotb.test()
async def test_forgecpu_tt1(dut):
    cocotb.start_soon(Clock(dut.clk, 100, unit="ns").start())
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await reset_cpu(dut)
    for a, b in enumerate([0x13,0x24,0x42,0xD0,0x70,0xC0,0x80,0xF0]):
        await load_byte(dut, a, b)
    await run_cycles(dut, 8)
    assert int(dut.uo_out.value) == 10
    dut.ui_in.value = 0x83; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 1
    dut.ui_in.value = 0x81; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 7
    dut.ui_in.value = 0x82; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 10

    await reset_cpu(dut)
    for a, b in enumerate([0x10,0xA4,0x19,0xF0,0x15,0x23,0x71,0xF0]):
        await load_byte(dut, a, b)
    await run_cycles(dut, 6)
    assert int(dut.uo_out.value) == 8
    dut.ui_in.value = 0x86; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 8
    dut.ui_in.value = 0x83; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 1

    await reset_cpu(dut)
    dut.ena.value = 1
    await load_byte(dut, 0, 0x10)
    dut.ena.value = 0
    await load_byte(dut, 0, 0x15)
    dut.ena.value = 1
    await load_byte(dut, 1, 0xF0)
    await run_cycles(dut, 1)
    assert int(dut.uo_out.value) == 0

    await reset_cpu(dut)
    dut.ena.value = 1
    await load_byte(dut, 0, 0x15)
    await load_byte(dut, 1, 0xF0)
    dut.ena.value = 0
    dut.ui_in.value = 0x40
    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")
    dut.ui_in.value = 0x81; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 0
    dut.ui_in.value = 0x80; await Timer(1, unit="ns")
    assert int(dut.uo_out.value) == 0
    dut.ena.value = 1
    await run_cycles(dut, 1)
    assert int(dut.uo_out.value) == 5

    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0
