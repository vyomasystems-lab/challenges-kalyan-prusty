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
    dut.Xin.value = int(32000/1.647) # 32000 is just a scaling factor and 1.647 is the gain of cordic algorithm
    dut.Yin.value = 0
    dut.angle.value = 0x2eeeeeee # (2^32 * (66/360)) equivalent value for 66 degrees

    #result will be available atlease after 16 clock cycles so we need to wait for it 
    for i in range(17): # this number can be anything more than 16
        await FallingEdge(dut.clock)
    
    # getting the exact value of output 
    cos_val = int(str(dut.Xout.value),2)
    sin_val = int(str(dut.Yout.value),2)
    print(f"COS(66) = {cos_val} & SIN(66) = {sin_val}")

    #converting the output into [-1,1] range
    cos_exact = cos_val/32000
    sin_exact = sin_val/32000
    print(f"COS(66) = {cos_exact} & SIN(66) = {sin_exact}")

