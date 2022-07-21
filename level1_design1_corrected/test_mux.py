# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random
import traceback

@cocotb.test()
async def test_mux_1(dut):
	"""Test-1 for mux2"""

	inp = [0]*31

	#setting up the 31 2-bit inputs 
	for i in range(31):
		inp[i] = 1 + (i % 3) # so all the inputs will be different from each other and will be from the set {1,2,3}
		print(f"inp{i} = {inp[i]}") # pinting the inputs to observe them

	# input driving for dut
	dut.inp0.value = inp[0]
	dut.inp1.value = inp[1]
	dut.inp2.value = inp[2]
	dut.inp3.value = inp[3]
	dut.inp4.value = inp[4]
	dut.inp5.value = inp[5]
	dut.inp6.value = inp[6]
	dut.inp7.value = inp[7]
	dut.inp8.value = inp[8]
	dut.inp9.value = inp[9]
	dut.inp10.value = inp[10]
	dut.inp11.value = inp[11]
	dut.inp12.value = inp[12]
	dut.inp13.value = inp[13]
	dut.inp14.value = inp[14]
	dut.inp15.value = inp[15]
	dut.inp16.value = inp[16]
	dut.inp17.value = inp[17]
	dut.inp18.value = inp[18]
	dut.inp19.value = inp[19]
	dut.inp20.value = inp[20]
	dut.inp21.value = inp[21]
	dut.inp22.value = inp[22]
	dut.inp23.value = inp[23]
	dut.inp24.value = inp[24]
	dut.inp25.value = inp[25]
	dut.inp26.value = inp[26]
	dut.inp27.value = inp[27]
	dut.inp28.value = inp[28]
	dut.inp29.value = inp[29]
	dut.inp30.value = inp[30]

	await Timer(2, units='ns')
	""" 
		1. This is a simple variable to count the number of errors it found 
		2. The number of times we are going into the exception block = number of errors
	"""
	count = 0
	for i in range(31):
		# Setting the select line to be at 12 i.e. sel = 5'b01100
		dut.sel.value = i
		await Timer(2,units = 'ns')

		try:
			assert dut.out.value == inp[i], "FAIL: 31x1 Multiplexer output when sel = {SEL} should be {INP_I} but the designed mux's output is {OUT}".format(SEL=i, INP_I=inp[i], OUT=dut.out.value)
		except Exception as msg:
			count = count + 1 # increase the count when there is a mismatch between actual output and expected output
			print(msg)
		
	assert count == 0, "count is {COUNT}, i.e. there are {COUNT} errors in the program".format(COUNT = count)

