// reverb.v

module reverb (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);

    parameter DELAY_LENGTH = 24000;
    parameter MIX_SHIFT = 2;

    reg signed [15:0] delay_buffer[0:DELAY_LENGTH-1];
    reg [14:0] index = 0;

    reg signed [15:0] delayed_sample;

    always @(posedge clk) begin
        delayed_sample <= delay_buffer[index];

        if (enable)
            out_sample <= in_sample + (delayed_sample >>> MIX_SHIFT);  // reverb mix
        else
            out_sample <= in_sample;  // bypass

        delay_buffer[index] <= in_sample;
        index <= (index + 1) % DELAY_LENGTH;
    end
endmodule
