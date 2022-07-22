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
    """ Some non sequence of 0's before the actual sequence. for eg. 0..0 1011 0..0"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    dut.inp_bit.value = 0 
    clk_time = 10 #clock time period

    # reset
    dut.reset.value = 1 #maintaing the reset value for 2 falling cloc edges so that there is a positive edge in between.
    await FallingEdge(dut.clk)  
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 0   #0
    time = 0
    
    await FallingEdge(dut.clk) 
    dut.inp_bit.value = 0   #10
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #20
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #30
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #40
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #50
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #60
    time = time + clk_time

    #actual output is in between 65 to 75 : so check the value of state and output in between i.e. 70
    #expected output is between 75 to 85 (as in the description it has to be delayed by one cycle) : so check the value of state and output in between i.e. 80
    
    await FallingEdge(dut.clk)  #70 
    time = time + clk_time
    dut.inp_bit.value = 0  
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    await FallingEdge(dut.clk) #80
    time = time + clk_time
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    assert (dut.seq_seen.value == 1) ,"output is {SEQ_SEEEN}, when current_state is {CUR_STATE}".format(SEQ_SEEEN = dut.seq_seen.value, CUR_STATE = dut.current_state.value)
    cocotb.log.info('#### CTB: Develop your test here! ######')

@cocotb.test()
async def test_seq_bug2(dut):
    """Some non sequence 1's before the actual sequence. for eg. 0111 1011 0.."""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    dut.inp_bit.value = 0 
    clk_time = 10 #clock time period

    # reset
    dut.reset.value = 1 #maintaing the reset value for 2 falling cloc edges so that there is a positive edge in between which ensure the reset
    await FallingEdge(dut.clk)  
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 1   #0
    time = 0
    
    await FallingEdge(dut.clk) 
    dut.inp_bit.value = 1   #10
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #20
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #30
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #40
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #50
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #60
    time = time + clk_time

    #actual output is in between 65 to 75 : so check the value of state and output in between i.e. 70
    #expected output is between 75 to 85 (as in the description it has to be delayed by one cycle) : so check the value of state and output in between i.e. 80
    
    await FallingEdge(dut.clk)  #70 
    time = time + clk_time
    dut.inp_bit.value = 0  
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    await FallingEdge(dut.clk) #80
    time = time + clk_time
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    assert (dut.seq_seen.value == 1) ,"output is {SEQ_SEEEN}, when current_state is {CUR_STATE}".format(SEQ_SEEEN = dut.seq_seen.value, CUR_STATE = dut.current_state.value)

@cocotb.test()
async def test_seq_bug3(dut):
    """  2 set of detecting sequence(1011) one after another. """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    dut.inp_bit.value = 0 
    clk_time = 10 #clock time period

    # reset
    dut.reset.value = 1 #maintaing the reset value for 2 falling cloc edges so that there is a positive edge in between which ensure the reset
    await FallingEdge(dut.clk)  
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 0   #0
    time = 0
    
    await FallingEdge(dut.clk) 
    dut.inp_bit.value = 0   #10
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #20
    time = time + clk_time
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #30
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0   #40
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #50
    time = time + clk_time

    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   #60
    time = time + clk_time

    #actual output is in between 65 to 75 : so check the value of state and output in between i.e. 70
    #expected output is between 75 to 85 (as in the description it has to be delayed by one cycle) : so check the value of state and output in between i.e. 80
    
    await FallingEdge(dut.clk)  #70 
    time = time + clk_time
    dut.inp_bit.value = 1
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    await FallingEdge(dut.clk)  #80 
    time = time + clk_time
    dut.inp_bit.value = 0
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    await FallingEdge(dut.clk)  #90 
    time = time + clk_time
    dut.inp_bit.value = 1

    await FallingEdge(dut.clk)  #100 
    time = time + clk_time
    dut.inp_bit.value = 1

    await FallingEdge(dut.clk)  #110 
    time = time + clk_time
    dut.inp_bit.value = 0

    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    await FallingEdge(dut.clk) #120
    time = time + clk_time
    print(f"Now Time is {time} and current_state is {dut.current_state.value}")
    print(f"Now Time is {time} and output is {dut.seq_seen.value}")

    assert (dut.seq_seen.value == 1) ,"output is {SEQ_SEEEN}, when current_state is {CUR_STATE}".format(SEQ_SEEEN = dut.seq_seen.value, CUR_STATE = dut.current_state.value)