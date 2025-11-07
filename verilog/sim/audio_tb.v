// audio_tb.v
`timescale 1ns/1ps

module audio_tb;

    // === Parameters ===
    //parameter NUM_SAMPLES = 1470000;   // 30 sec @ 48kHz __ this is for C-Scale
    //parameter NUM_SAMPLES = 3546112; // ~73.8 sec @ 48kHz __ this is for Aiman solo
    //parameter NUM_SAMPLES = 480000;  // 10 sec @ 48kHz __ this is for the synthetics we made
    parameter NUM_SAMPLES = 3619902;   // full length of Miniature Etude no 4.mem
    parameter FRAME_SIZE = 1000;       // Log every 1000 samples

    // === Signals ===
    reg clk = 0;

    reg global_enable = 1;
    reg enable_reverb = 0;
    reg enable_tone_filter = 0;
    reg enable_resonator = 1;
    reg enable_autotune = 1;
    reg enable_noise_gate = 1;
    reg enable_warmer = 1;
    reg enable_envelope = 0; // rn sounds robotic no good bad
    reg enable_compressor = 1;
    reg enable_exciter = 0;

    reg signed [15:0] samples[0:NUM_SAMPLES-1];
    reg signed [15:0] in_sample;
    wire signed [15:0] out_sample;
    wire [15:0] est_freq;
    wire [15:0] target_freq;

    integer i;
    integer outfile;
    integer pitchfile;
    integer frame_counter = 0;

    // === DUT ===
    audio_processor dut (
        .clk(clk),
        .global_enable(global_enable),
        .enable_reverb(enable_reverb),
        .enable_tone_filter(enable_tone_filter),
        .enable_resonator(enable_resonator),
        .enable_autotune(enable_autotune),
        .enable_noise_gate(enable_noise_gate),
        .enable_warmer(enable_warmer),
        .enable_envelope(enable_envelope),
        .enable_compressor(enable_compressor),
        .enable_exciter(enable_exciter),
        .in_sample(in_sample),
        .out_sample(out_sample),
        .est_freq(est_freq),
        .target_freq(target_freq)
    );

    // === Clock generator ===
    always #1 clk = ~clk;

    // === Main simulation ===
    initial begin
        $display("Loading input samples...");
        //$readmemb("C-Scale.mem", samples); // Change this file for different input audio
        //$readmemb("Solo Trumpet Performance by Airman.mem", samples);
        $readmemb("Miniature Etude no 4.mem", samples);
        
        outfile = $fopen("processed_output.mem", "w");
        pitchfile = $fopen("pitch_log.csv", "w");
        $fwrite(pitchfile, "frame_num,estimated_freq,target_freq\n");

        $display("Processing samples...");
        for (i = 0; i < NUM_SAMPLES; i = i + 1) begin
            in_sample = samples[i];
            @(posedge clk);
            $fwrite(outfile, "%d\n", out_sample);

            if (i % FRAME_SIZE == 0) begin
                $fwrite(pitchfile, "%0d,%0d,%0d\n", frame_counter, est_freq, target_freq);
                frame_counter = frame_counter + 1;
            end
        end

        $fclose(outfile);
        $fclose(pitchfile);
        $display("✅ Simulation complete. Output files written.");
        $finish;
    end

endmodule
