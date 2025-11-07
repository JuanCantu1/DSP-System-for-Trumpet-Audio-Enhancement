// noise_gate.v

module noise_gate (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);

    parameter THRESHOLD = 1000;      // Lower to let soft brass pass
    parameter HOLD_TIME = 3000;      // Longer hold = fewer cutoffs
    parameter FADE_SHIFT = 1;        // Right shift on fade (>>= 1 = halve)

    reg [15:0] hold_counter = 0;
    reg gate_open = 0;

    always @(posedge clk) begin
        if (enable) begin
            if (in_sample > THRESHOLD || in_sample < -THRESHOLD) begin
                gate_open <= 1;
                hold_counter <= 0;
                out_sample <= in_sample;
            end else begin
                if (gate_open) begin
                    if (hold_counter < HOLD_TIME) begin
                        hold_counter <= hold_counter + 1;
                        out_sample <= in_sample;
                    end else begin
                        gate_open <= 0;
                        out_sample <= out_sample >>> FADE_SHIFT;  // soft fade-out
                    end
                end else begin
                    // Fade out completely to 0 over time
                    if (out_sample != 0)
                        out_sample <= out_sample >>> FADE_SHIFT;
                    else
                        out_sample <= 0;
                end
            end
        end else begin
            out_sample <= in_sample;
        end
    end
endmodule
