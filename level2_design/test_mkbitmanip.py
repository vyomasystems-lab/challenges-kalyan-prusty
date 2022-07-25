# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # func7 and func3 are only for type-1 testcases
    func7 = ["0100000", "0100000", "0100000", "0010000", "0010000", "0110000", "0110000", "0010000", "0010000","0010000","0100100","0010100","0110100","0100100","0010100","0110100","0100100","0000100","0000100","0000101","0000101","0000101","0000101","0000101","0000101","0000101","0100100","0000100","0000100","0100100","0000100"]
    func3 = ["111","110","100","001","101","001","101","010","100","110","001","001","001","101","101","101","111","001","101","001","011","010","100","101","110","111","110","110","100","100","111"]
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0110011"
    error_count = 0
    for i in range(len(func7)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7[i] + rs2 + rs1 + func3[i] + rd + opcode
        # input transaction
        mav_putvalue_src1 = 0x7
        mav_putvalue_src2 = 0x8
        mav_putvalue_src3 = 0x9
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        printf(f"This is {i}th itteration.")
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
    
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print(f"Number of error is {error_count}")


@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7_2bit = ["11","11","10","10"]
    func3 = ["001","101","001","101"]
    rs3 = "00000"
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0110011"
    error_count = 0
    for i in range(len(func3)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7[i] + rs2 + rs1 + func3[i] + rd + opcode
        # input transaction
        mav_putvalue_src1 = 0x7
        mav_putvalue_src2 = 0x8
        mav_putvalue_src3 = 0x9
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        printf(f"This is {i}th itteration.")
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
    
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print(f"Number of error is {error_count}")
