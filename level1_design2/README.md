# Level1_Design1 (Sequence Detector) Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![main_failure](https://user-images.githubusercontent.com/33130256/180493834-88c83a9a-8264-463d-9d39-00a811a92146.png)

## Verification Environment
The CoCoTb based Python test is developed as explained. The test drives inputs to the Design Under Test (seq_detect_1011.v module here) which takes in 1-bit input **inp_bit,
clk** and **reset** and generates 1-bit output **seq_seen**.

**clk** to the provided as follows:
```
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
```
Before providing any input bits we first set the FSM to the known state i.e. IDLE so that we can predict the behaviour and this is done by the help of **reset** input as follows:
```
    # reset
    dut.reset.value = 1 #maintaing the reset value for 2 falling cloc edges so that there is a positive edge in between which ensure the reset
    await FallingEdge(dut.clk)  
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)
```
And after this input sequence is provided to the system using the following code block:
```
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
```
In the code above **time** variable is continuously increased according to the input change. And the **await** statements are used to get to the precise location of the clock
edges. And finally the **printf** statements are used to show the **current state** and output **seq_seen**.

The following **assert** statements are used to check the output after providing all the input and waiting for one more clock cycle (as shown in the video).
```
 assert (dut.seq_seen.value == 1) ,"output is {SEQ_SEEEN}, when current_state is {CUR_STATE}".format(SEQ_SEEEN = dut.seq_seen.value, CUR_STATE = dut.current_state.value)
```

In the above we have seen code for clock generation, providing input and checking the output at right time only for one particular case for bug finding (Failed Case - 1).
Similar to this for other 2 buggy cases we can provide similar input and check for the output.

## Test Scenario
### Failed Case - 1
-  Here the input i.e. **inp_bit** is some non sequence 0's before the actual sequence. for eg. 0000**1011**00. Each bit is provided on every clock edge. Reset is continuously 0 for the whole time.
-  Expected output and Actual output is shown in the following waveform.
![wavedrom_bug1](https://user-images.githubusercontent.com/33130256/180498912-8db51826-34b6-4457-ae55-85162b35425c.png)
#### Observation
Expected output waveform is just a shifted form of the actual output waveform which proves that there is a bug in the design.

### Failed Case - 2
-  Here the input i.e. **inp_bit** is some non sequence 1's before the actual sequence. for eg. 0111**1011**00. Each bit is provided on every clock edge. Reset is continuously 0 for the whole time.
-  Expected output and Actual output is shown in the following waveform.
![wavedrom_bug2](https://user-images.githubusercontent.com/33130256/180499890-e4c40dbd-e161-4591-a252-b3f648e9a8c5.png)

#### Observation
Expected output waveform has a pulse which is absent in the actual output which proves that there is a bug in the design.

### Failed Case - 3
-  Here the input i.e. **inp_bit** is similar to the case - 1 but after the detecting sequence(**1011**) we have another detecting sequence. for eg. 0000**10111011**00. Each bit is provided on every clock edge. Reset is continuously 0 for the whole time.
-  Expected output and Actual output is shown in the following waveform.
![wavedrom_bug3](https://user-images.githubusercontent.com/33130256/180506456-f37d1d33-d3d0-4a0d-8d87-d95325d1038f.png)

#### Observation
Expected output waveform has 2 pulse where as one is absent in the actual output which proves that there is a bug in the design.

## Design Bug
### Bug - 1
```
  // if the current state of the FSM has the sequence 1011, then the output is
  // high
  assign seq_seen = current_state == SEQ_1011 ? 1 : 0;                        <===== BUG - 1
```
Here the moore machine generates output when the current state is SEQ_1011 using a simple combinational multiplexer. But the specification tells that the output need to be delayed bu one clock cycle.
Hence to solve this problem we can pass current output through a D-flip flop (latch our output **seq_seen**).

### Bug - 2
```
  SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;                            <==== BUG - 2
        else
          next_state = SEQ_10;
      end
```
Here when the FSM is in **SEQ_1** state and another **logic-1** comes at the input then it moves to **IDLE** state which restarts the sequence detector again that should not be the case.
As we have recieved one **1** then we should be in the same state unless any **0** comes in the input stream.

### Bug - 3
```
  SEQ_1011:
      begin
        next_state = IDLE;                               <==== BUG - 3
      end
```
Here when the FSM is in **SEQ_1011** state and irrespective of the input it directly goes to **IDLE** state which is not correct. If the FSM is in **SEQ_1011** and a **1** comes then
that should be considered as the initial **1** of the detecting sequence and FSM should go to **SEQ_1** and for **0** it should move to **IDLE** state.

## Design Fixs
### Fix - 1
The output should be latched.
```
  wire seq_seen_internal;
  assign seq_seen_internal = current_state == SEQ_1011 ? 1 : 0;  
  always@(posedge clk)
      seq_seen = seq_seen_internal;                           <===== FIX - 1
```

### Fix - 2
On **inp_bit**  = 1 FSM should stay in the same state if FSM is in **SEQ_1**.
```
  SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;                            <==== FIX - 2
        else
          next_state = SEQ_10;
      end
```

### Fix - 3
if FSM is in **SEQ_1011** state then depending on **inp_bit** it should change it's state.
```
  SEQ_1011:
      begin
         if(inp_bit == 1)
          next_state = SEQ_1;                            <==== FIX - 3
        else
          next_state = IDLE;
      end
```
