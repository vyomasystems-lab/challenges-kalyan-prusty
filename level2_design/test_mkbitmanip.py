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

src1 = 0x7
src2 = 0x56
src3 = 0x32
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
def run_test_1(dut):
    
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
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 1")
    print(f"Number of error is {error_count}")


@cocotb.test()
def run_test_2(dut):
    
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
        inst_str = rs3 + func7_2bit[i] + rs2 + rs1 + func3[i] + rd + opcode
        # input transaction
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 2")
    print(f"Number of error is {error_count}")

@cocotb.test()
def run_test_3(dut):
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7 = "0110000"
    func3 = "001"
    imm_value_1 = ["00000","00001","00010","00100","00101","10000","10001","10010","11000","11001","11010"]
    rs1 = "00000"
    rd = "00000"
    opcode = "0010011"
    error_count = 0
    for i in range(len(imm_value_1)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7 + imm_value_1[i] + rs1 + func3 + rd + opcode
        # input transaction
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 3")
    print(f"Number of error is {error_count}")

@cocotb.test()
def run_test_4(dut):
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7_imm = ["00100","01001","00101","01101","01001"]
    func3 = ["001","001","001","001","101"]
    func7_2bit = "00"
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0010011"
    error_count = 0
    for i in range(len(func3)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7_imm[i] + func7_2bit + rs2  + rs1 + func3[i] + rd + opcode
        # input transaction
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 4")
    print(f"Number of error is {error_count}")

@cocotb.test()
def run_test_5(dut):
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7_imm = ["00100","01100","00101","01101"]
    func3 = "101"
    func7_2bit = "00"
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0010011"
    error_count = 0
    for i in range(len(func7_imm)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7_imm[i] + func7_2bit + rs2  + rs1 + func3 + rd + opcode
        # input transaction
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 5")
    print(f"Number of error is {error_count}")


@cocotb.test()
def run_test_6(dut):
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7_imm_SHFL = "000010"
    func3 = ["001","101"]
    func7_1bit = "0"
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0010011"
    error_count = 0
    for i in range(len(func3)): # as there are 31 elements in the func7 and func3 arrays
        inst_str = func7_imm_SHFL + func7_1bit + rs2  + rs1 + func3[i] + rd + opcode
        # input transaction
        mav_putvalue_src1 = src1
        mav_putvalue_src2 = src2
        mav_putvalue_src3 = src3 
        mav_putvalue_instr = int(inst_str, 2)

        # expected output from the model
        #print(f"This is {i}th itteration.")
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

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if(dut_output != expected_mav_putvalue) :
            error_count = error_count + 1;
            print(error_message)
    print("TEST SET 6")
    print(f"Number of error is {error_count}")

@cocotb.test()
def run_test_7(dut):
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    func7_5bit = "00000"
    func7_fsri_1bit = "1"
    func7_1bit = "0"

    func3 = "101"
    
    rs2 = "00000"
    rs1 = "00000"
    rd = "00000"
    opcode = "0010011"
    error_count = 0
    
    inst_str = func7_5bit + func7_fsri_1bit + func7_1bit + rs2 + rs1 + func3 + rd + opcode
    # input transaction
    mav_putvalue_src1 = src1
    mav_putvalue_src2 = src2
    mav_putvalue_src3 = src3 
    mav_putvalue_instr = int(inst_str, 2)

    # expected output from the model
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

    #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
    # comparison
    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    if(dut_output != expected_mav_putvalue) :
        error_count = error_count + 1;
        print(error_message)
    print("TEST SET 7")
    print(f"Number of error is {error_count}")