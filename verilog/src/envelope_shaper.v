// envelope_shaper.v
// ----------------------------------
// Attack-Release envelope follower for smooth, natural trumpet phrasing
// Implements dynamic gain (no smoothing of waveform), preserving tone
// ----------------------------------

module envelope_shaper (
    input  wire         clk,
    input  wire         enable,
    input  signed [15:0] in_sample,
    output reg   signed [15:0] out_sample
);

    // === Parameters ===
    parameter [7:0] ATTACK_STEP   = 8'd8;       // ramp-up speed (higher = faster)
    parameter [7:0] RELEASE_STEP  = 8'd4;       // ramp-down speed
    parameter signed [15:0] THRESHOLD = 16'sd100; // input level to consider "note on"
    parameter [7:0] MIN_GAIN      = 8'd64;      // floor at 25% gain (Q8)

    // === Internal State ===
    reg [7:0] gain_reg = MIN_GAIN;               // Q8 dynamic gain
    wire signed [15:0] abs_in = in_sample[15] ? -in_sample : in_sample;
    // Multiply signed sample by signed gain (extended) → 24-bit
    wire signed [23:0] mult_val = in_sample * $signed({1'b0, gain_reg});

    always @(posedge clk) begin
        if (enable) begin
            // Envelope detector
            if (abs_in > THRESHOLD) begin
                // Note ON: ramp up to max
                gain_reg <= (gain_reg + ATTACK_STEP > 8'd255) ? 8'd255 : gain_reg + ATTACK_STEP;
            end else begin
                // Note OFF: ramp down to MIN_GAIN floor
                gain_reg <= (gain_reg > MIN_GAIN + RELEASE_STEP) ? gain_reg - RELEASE_STEP : MIN_GAIN;
            end
            // Apply dynamic gain and scale back (Q8 → Q0)
            out_sample <= mult_val >>> 8;
        end else begin
            // Bypass
            gain_reg   <= 8'd255;
            out_sample <= in_sample;
        end
    end

endmodule
