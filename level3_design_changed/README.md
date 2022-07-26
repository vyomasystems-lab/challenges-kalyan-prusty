# Level3_Design_Changed (Wrong Design) (CORDIC IP for sine and cosine value of any given angle) Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
![overall_fail](https://user-images.githubusercontent.com/33130256/181612585-7c7ca35d-dd49-4359-811a-2eb8d2ae8158.png)

## Error introduced in the Design
In the correct design the cordic equation was as follows:
```
         // add/subtract shifted data
         X[i+1] <= Z_sign ? X[i] + Y_shr         : X[i] - Y_shr;
         Y[i+1] <= Z_sign ? Y[i] - X_shr         : Y[i] + X_shr;
         Z[i+1] <= Z_sign ? Z[i] + atan_table[i] : Z[i] - atan_table[i];
```
To intoduce error in the desin i have changed the actual cordic equations as follows:
```
        // add/subtract shifted data
         X[i+1] <= Z_sign ? X[i] + Y_shr         : X[i] - Y_shr;
         Y[i+1] <= Z_sign ? Y[i] + X_shr         : Y[i] - X_shr;
         Z[i+1] <= Z_sign ? Z[i] + atan_table[i] : Z[i] - atan_table[i];
```
Observe the *Y[i+1]* equation in both the cases.

## Description of Design 
The implemented design in CORDIC.v file takes following inputs
```
    1. Xin: Initial x-coordinator of Vector [32-bit]
    2. Yin: Initial y-coordinator of Vector [32-bit]
    3. Angle: theta for which we want to find cosine or sine [32-bit]
```
But for proper analysis the Xin is 32000/1.674 and Yin is 0. As Xin is 32000/1.647 the output will be *32000 x cos(angle)* instead of *cos(angle)* and similarly for sine.
Here 1.647 is the gain that is automatically generated during the CORDIC calculation.[Described in Initial Report].

Similar to Xin and Yin the angle has some specific requirments.The whole 360° is mapped to 0 to 2^32. For eg. to represent 66°:
Angle = 2^32 * (66/360);

The Design in this folder is a correct design without any introduction of error. As in the actual design the designer has implemented a pipelined arch. of 16 stages, for 
observing the 1st output form the design we need to wait for atleast 16 cycles as described here:
```
 for i in range(17): # this number can be anything more than 16
        await FallingEdge(dut.clock)
```
## Verification Environment
The input to the design is provided as follows:
```
    #defining all the inputs 
    dut.Xin.value = int(32000/1.647) # 32000 is just a scaling factor and 1.647 is the gain of cordic algorithm
    dut.Yin.value = 0
    dut.angle.value = 0x2eeeeeee # (2^32 * (66/360)) equivalent value for 66 degrees
```

After this we have to wait for atleast 16 clock cycles to read the output from the design. The output we will be reading 
is in binary format which is convered to integer as follows
```
    # getting the exact value of output 
    cos_val = int(str(dut.Xout.value),2)
    sin_val = int(str(dut.Yout.value),2)
    print(f"COS(66) = {cos_val} & SIN(66) = {sin_val}")
```
This is scaled value of cos(66) and sin(66). To convert this into proper range i.e. [-1,1] we have to divided by the scaling factor which is 32000.
```
    #converting the output into [-1,1] range
    cos_exact = cos_val/32000
    sin_exact = sin_val/32000
    print(f"COS(66) = {cos_exact} & SIN(66) = {sin_exact}")
```
Let's check the output with the expected values of output
```
assert ((cos_val == 13011) and (sin_val == 29230)), "There is some error in the design as design is not working as expected"
```
![image](https://user-images.githubusercontent.com/33130256/181612160-731f4b26-1572-4af3-8aad-cf89c77b1cba.png)

After ececuting this we can observe that the values are different from the expected values.

