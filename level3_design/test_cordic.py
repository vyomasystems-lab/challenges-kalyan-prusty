import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_cordic_bug1(dut):
    clock = Clock(dut.clock, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    #defining all the inputs 
    dut.Xin.value = 32000/1.647
    dut.Yin.value = 0
    dut.angle.value = 0x2eeeeeee # (2^32 * (66/360)) equivalent value for 66 degrees

    #result will be available atlease after 16 clock cycles so we need to wait for it 
    for i in range(18): # this number can be anything more than 16
        await FallingEdge(dut.clk)
    
    print(f"SIN(66) = {dut.Xout.value} & COS(66) = {dut.Xout.value}")

