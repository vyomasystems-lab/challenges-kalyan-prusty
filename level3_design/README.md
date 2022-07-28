# Level3_Design (CORDIC IP for sine and cosine value of any given angle) Design Verification

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
After ececuting this we can recieve the values as follows:
![value ](https://user-images.githubusercontent.com/33130256/181610311-749fcb89-8f30-4299-9da3-b669df383bb1.png)
Let's check on calculator it on calculator to verify.
![image](https://user-images.githubusercontent.com/33130256/181612986-e4616505-e632-49e1-86e7-5c720619a3af.png)


So After intoducing the bug we can check whether cosine and sine value are 13011 and 29230 respectively or not?
