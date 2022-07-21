# Level1_Design1 (Multiplexer) Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![MUX_fail](https://user-images.githubusercontent.com/33130256/180129624-36ffa5ea-7262-4358-9a65-ce3fb441a4da.png)

## Verification Environment
The CoCoTb based Python test is developed as explained. The test drives inputs to the Design Under Test (mux.v module here) which takes in 31 2-bit inputs 
*inp0, inp1 ... inp30* and sel which is a 5-bit input and finaly gives 5-bit output *out*.

The values are assigned to the input port using
```
  inp = [0]*31

	#setting up the 31 2-bit inputs 
	for i in range(31):
		inp[i] = 1 + (i % 3) # so all the inputs will be different from each other and will be from the set {1,2,3}, 
		print(f"inp{i} = {inp[i]}") # printing the inputs to observe them

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

```

The assert statement is used for comparing the multiplexer's outut to the expected value. If the output of mux is not matched then the python code will increase the 
number of error counting and finally if the number of errors is more than 0 then the python 

The following error is seen:
```
  try:
    assert dut.out.value == inp[i], "FAIL: 31x1 Multiplexer output when sel = {SEL} should be {INP_I} but the designed mux's output is {OUT}".format(SEL=i, INP_I=inp[i], OUT=dut.out.value)
  except Exception as msg:
    count = count + 1 # increase the count when there is a mismatch between actual output and expected output
    print(msg)
```
And finally the value of count is compared with 0 and if not then it is asserted by 
```
  assert count == 0, "count is {COUNT}, i.e. there are {COUNT} errors in the program".format(COUNT = count)
```

## Test Scenario
![reason_mux_fail](https://user-images.githubusercontent.com/33130256/180140634-4b47e172-e9bf-4381-a380-7fe7792f91fd.png)

This screen shot is taken from the terminal window where all the 3 failing test cases are shown along with the input.

**Note: For all the cases inputs inp0,inp1...inp30 are same and highlighted in a green box in the above image.**

### Failed Case-1
- sel [Input] = 12
- Expected output = inp12 = 1
- out [Actual Output] = 0
Output mismatches for the above inputs proving that there is a design bug.

### Failed Case-2
- sel [Input] = 13
- Expected output = inp13 = 2
- out [Actual Output] = 1
Output mismatches for the above inputs proving that there is a design bug.

### Failed Case-3
- sel [Input] = 30
- Expected output = inp30 = 1
- out [Actual Output] = 0
Output mismatches for the above inputs proving that there is a design bug.

## Design Bug
### Bug-1
```
    case(sel)
      5'b00000: out = inp0;  
      .
      .
      5'b01011: out = inp11;                        
      5'b01101: out = inp12;                          ====> BUG
      5'b01101: out = inp13;
      .
      .
      default: out = 0;
    endcase
```
Here there is no case that will be satisfied for sel = 5'b01100. Hence, the case statement is satified for the default case and making the out = 0

### Bug-2
```
    case(sel)
      5'b00000: out = inp0;  
      .
      .
      5'b01011: out = inp11;                        
      5'b01101: out = inp12;                          ====> BUG
      5'b01101: out = inp13;                          ====> BUG
      .
      .
      default: out = 0;
    endcase
```
Here there 2 cases that is going to satisfy for sel = 5'b01101. But as it is a case statement so the 1st case is matched i.e.
```
      5'b01101: out = inp12;
```
Hence there is a mismatch in the output.

### Bug-3
```
    case(sel)
      5'b00000: out = inp0;  
      .
      .
      .
      5'b11100: out = inp28;                        
      5'b11101: out = inp29;                        
      default: out = 0;                     ====> BUG
    endcase
```
Here there is no case that is going to satisfied if sel = 5'b11110. Hence, the case statement is satified for the default case and making the out = 0. 

## Design Fix
### Design Fix for Bug - 1&2
We need to change  ``5'b01101: out = inp12;`` to ``5'b01100: out = inp12;``.
```
  case(sel)
      5'b00000: out = inp0;  
      .
      .
      5'b01011: out = inp11;                        
      5'b01100: out = inp12;                          ====> BUG FIX - 1&2
      5'b01101: out = inp13;                          
      .
      .
      default: out = 0;
    endcase
```
### Design Fix for Bug - 3
Write   ``5'b11110: out = inp30;`` in the case statement.
```
    case(sel)
      5'b00000: out = inp0;  
      .
      .
      .
      5'b11100: out = inp28;                        
      5'b11101: out = inp29;        
      5'b11110: out = inp30;                    ===> BUG FIX - 3
      default: out = 0;
    endcase
```
