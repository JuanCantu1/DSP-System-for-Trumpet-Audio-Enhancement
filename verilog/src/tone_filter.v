// tone_filter.v

module tone_filter (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);

    parameter SHIFT = 2;  // Controls strength of smoothing

    reg signed [15:0] previous = 0;

    always @(posedge clk) begin
        if (^in_sample === 1'bx) begin
            out_sample <= 16'sd0;
        end else if (enable) begin
            previous <= previous + ((in_sample - previous) >>> SHIFT);
            out_sample <= previous;
        end else begin
            out_sample <= in_sample;
        end
    end

endmodule
