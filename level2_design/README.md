# Level2_Design (Bit manipulation Coprocessor) Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
![main_fail](https://user-images.githubusercontent.com/33130256/181161766-581275cc-5f48-43b3-8b5b-aa4f75f5b855.png)

Here we can observe that from all the seven tests [All the possible tests are divided into 7 test cases] we ran one [run_test_1()] has been failed and others are passed.

## Verification Environment
As there are several instructions to check. But here it is divided into 7 smaller test cases as follows according to the type of instructions i.e. R-type, I-type etc. So
that it will be easier to loop over all same type instruction with random inputs at one go. Different sets are as follows:

```
SET-1:
All instructions which satisfy
((func7 == "0100000") and (func3 == "111") and (opcode == "0110011"))
There are 31 instruction which satisfy this criteria.

SET-2:
All instructions which satisfy
((func7_2bit == "11") and (func3 == "001") and (opcode == "0110011"))
There are 4 instruction which satisfy this criteria.

SET-3:
All instructions which satisfy
((func7 == "0110000") and (imm_value_1 == "00000") and (func3 == "001") and (opcode == "0010011"))
There are 11 instruction which satisfy this criteria.

SET-4:
All instructions which satisfy
((func7_imm == "00100")  and (func3 == "001") and (opcode == "0010011"))
There are 5 instruction which satisfy this criteria.

SET-5:
All instructions which satisfy
((func7_imm == "00100") and (func7_fsri_1bit != "1") and (func3 == "101") and (opcode == "0010011"))
There are 4 instruction which satisfy this criteria.

SET-6:
All instructions which satisfy
((func7_imm_SHFL == "000010")  and (func3 == "001") and (opcode == "0010011"))
There are 2 instruction which satisfy this criteria.

SET-7:
All instructions which satisfy
((func7_fsri_1bit == "1")  and (func3 == "101") and (opcode == "0010011"))
There are 1 instruction which satisfy this criteria.
```
Hence by doing that we will be able to cover all the 58 instructions.
The CoCoTb based Python test is developed as explained. Here the instructions are taken one by as described above and using *random.randint(1, 100)* we are generating 
random numbers for all the inputs and assigned to the actual iputs as follows:
```
    # input transaction
    mav_putvalue_src1 = random.randint(1, 100)
    mav_putvalue_src2 = random.randint(1, 100)
    mav_putvalue_src3 = random.randint(1, 100) 
```
This input is provided to the python program which mimics the actual DUT [with out any bug].
```
expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
```
And the same input is also provided to actual dut.
```
    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    dut.mav_putvalue_instr.value = mav_putvalue_instr
```
After this the output of DUT is compared to the output of bitmanip python function output and along with this the last bit of DUT's output should be 1 for this to be 
a valid output. Then in all set total number of errornous instructions are counted.
```
    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    if(dut_output != expected_mav_putvalue or (not(dut_output & 0x1))) :
      error_count = error_count + 1
      print(error_message)
```
If the error_count is more than 0 then some of the instructions are not working as expected. So we need to assert at that point.
```
assert (error_count == 0), "There are {ERR_CNT} errors in this test case".format(ERR_CNT = error_count)
```
The same is done for all the test cases.

## Test Scenario
![fail_test_1](https://user-images.githubusercontent.com/33130256/181168096-429b2098-4c81-4611-a726-09edaafbd187.png)
Here we can see there is an error. And on analysing more we can see the error is in *ANDN instruction*.
![and_fail](https://user-images.githubusercontent.com/33130256/181169354-c3f3a86c-3a14-463c-b1cb-e5107aee2b7d.png)
In the above image we can observe 

