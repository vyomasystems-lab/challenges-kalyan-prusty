// See LICENSE.vyoma for more details
// Verilog module for Sequence detection: 1011
module seq_detect_1011(seq_seen, inp_bit, reset, clk);

  output reg seq_seen;
  input inp_bit;
  input reset;
  input clk;

  parameter IDLE = 0,
            SEQ_1 = 1, 
            SEQ_10 = 2,
            SEQ_101 = 3,
            SEQ_1011 = 4;

  reg [2:0] current_state, next_state;

  wire seq_seen_internal;
  // if the current state of the FSM has the sequence 1011, then the output is
  // high
  assign seq_seen_internal = current_state == SEQ_1011 ? 1 : 0;
  always@(posedge clk)
    seq_seen <= seq_seen_internal;                                  //BUG FIX - 1

  // state transition
  always @(posedge clk)
  begin
    if(reset)
    begin
      current_state <= IDLE;
    end
    else
    begin
      current_state <= next_state;
    end
  end

  // state transition based on the input and current state
  always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;                       //BUG FIX - 2
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;
      end
      SEQ_1011:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;                            //BUG FIX - 3
        else
          next_state = IDLE;
      end
    endcase
  end
endmodule
