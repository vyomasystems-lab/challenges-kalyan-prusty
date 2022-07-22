# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    dut.inp_bit.value = 0 

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 0   #0
    await FallingEdge(dut.clk) 
    dut.inp_bit.value = 0   #10
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #20
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #30
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #40
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #50
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #60

    #actual output is in between 65 to 75
    #expected output is between 75 to 85
    await FallingEdge(dut.clk)
    print(f"Now Time is 70 and output is {dut.seq_seen.value}")
    await RisingEdge(dut.clk)
    print(f"Now Time is 75 and output is {dut.seq_seen.value}")
    await FallingEdge(dut.clk)
    print(f"Now Time is 80 and output is {dut.seq_seen.value}")

    cocotb.log.info('#### CTB: Develop your test here! ######')
