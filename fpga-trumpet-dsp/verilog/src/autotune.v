// autotune.v

module autotune (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample,
    output reg [15:0] est_freq,
    output reg [15:0] target_freq
);

    parameter FRAME_SIZE = 1000;
    parameter SAMPLE_RATE = 48000;

    reg signed [15:0] prev_sample = 0;
    reg [15:0] zero_cross_count = 0;
    reg [15:0] sample_counter = 0;

    integer i;
    reg [15:0] freq, diff, best_diff;
    reg [4:0] best_note;

    function [15:0] get_note_freq;
        input [4:0] note_index;
        case (note_index)
            5'd0:  get_note_freq = 261;
            5'd1:  get_note_freq = 277;
            5'd2:  get_note_freq = 293;
            5'd3:  get_note_freq = 311;
            5'd4:  get_note_freq = 329;
            5'd5:  get_note_freq = 349;
            5'd6:  get_note_freq = 370;
            5'd7:  get_note_freq = 392;
            5'd8:  get_note_freq = 415;
            5'd9:  get_note_freq = 440;
            5'd10: get_note_freq = 466;
            5'd11: get_note_freq = 493;
            5'd12: get_note_freq = 523;
            5'd13: get_note_freq = 554;
            5'd14: get_note_freq = 587;
            5'd15: get_note_freq = 622;
            5'd16: get_note_freq = 659;
            5'd17: get_note_freq = 698;
            5'd18: get_note_freq = 740;
            5'd19: get_note_freq = 784;
            5'd20: get_note_freq = 831;
            5'd21: get_note_freq = 880;
            5'd22: get_note_freq = 932;
            5'd23: get_note_freq = 988;
            default: get_note_freq = 0;
        endcase
    endfunction

    always @(posedge clk) begin
        if (enable) begin
            if ((in_sample[15] != prev_sample[15]) &&
                (in_sample != 0 && prev_sample != 0)) begin
                zero_cross_count <= zero_cross_count + 1;
            end
            prev_sample <= in_sample;

            sample_counter <= sample_counter + 1;
            if (sample_counter == FRAME_SIZE) begin
                est_freq <= (zero_cross_count * (SAMPLE_RATE / 2)) / FRAME_SIZE;

                best_diff = 16'hFFFF;
                best_note = 0;
                for (i = 0; i < 24; i = i + 1) begin
                    freq = get_note_freq(i);
                    diff = (est_freq > freq) ? (est_freq - freq) : (freq - est_freq);
                    if (diff < best_diff) begin
                        best_diff = diff;
                        best_note = i[4:0];
                    end
                end

                target_freq <= get_note_freq(best_note);
                zero_cross_count <= 0;
                sample_counter <= 0;
            end

            out_sample <= in_sample; // Replace with processed signal if available
        end else begin
            out_sample <= in_sample;
            est_freq <= 0;
            target_freq <= 0;
        end
    end
endmodule
