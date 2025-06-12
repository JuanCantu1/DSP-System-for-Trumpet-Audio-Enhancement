# 🎺 FPGA-Based Digital Signal Processor for Trumpet Audio Enhancement

## 📌 Overview

This project aims to build a real-time **audio enhancement system for trumpet** using an FPGA platform (DE1-SoC). The work is divided into three integrated phases:

1. **Phase 1 – Pitch Detection System on HPS** ✅ *(Completed)*
   Real-time frequency detection and note-mapping using Python running on the ARM Cortex-A9 (HPS).

2. **Phase 2 – Real-Time DSP on FPGA** 🔄 *(In Progress)*
   Verilog-based DSP effects (reverb, echo removal, pitch correction) implemented on the Cyclone V FPGA.

3. **Phase 3 – Integrated System** 🔜 *(Planned)*
   Combines Phase 1 and Phase 2 into a full-stack real-time audio enhancement pipeline.

---

## 🎬 Demo

🎥 **Watch the system in action**  
📁 `Demo.mp4` — Demonstrates live pitch detection, note mapping, and real-time graphing.  
🔊 **Make sure your volume is on!**

<video src="https://github.com/user-attachments/assets/2d0dee5a-57bc-4de3-bd50-d095a3c48c55" controls width="600"></video>

---

## 📡 Phase 1: Pitch Detection System (Completed)

This subproject serves as a proof of concept for accurate trumpet pitch detection. It establishes the foundation for audio input capture, note recognition, and network-based data transmission.

### 🎯 Goals

* Capture trumpet audio via microphone.
* Use Python to extract **fundamental frequencies** (YIN algorithm).
* Map detected frequencies to **concert** and **trumpet-transposed (Bb)** notes.
* Analyze results using mean, standard deviation, and 95% CI.
* Generate annotated frequency graphs.
* Transmit frequency data over TCP/IP.

### 🧪 Outputs

* `frequency_log.csv`: Frequency and note mapping data
* `frequency_graph.png`: Annotated graph of pitch over time
* `raw_audio.wav`: Raw audio captured by the server and transmitted to the client

---

## 🔧 Phase 2: Real-Time DSP on FPGA (In Progress)

This phase focuses on developing a real-time **digital signal processor** (DSP) fully in Verilog to process trumpet audio using the Cyclone V FPGA fabric on the DE1-SoC.

We are **not using the HPS in this phase**. The input audio is provided as `.mem` files (converted from `.wav`), and the output is analyzed via simulation, waveform/spectrogram tools, and listening tests.

### 🎧 DSP Modules (Verilog)

Each module operates on a streaming, sample-by-sample basis. Effects can be selectively enabled via control signals.

| Module        | Functionality                                           | Enable Control         |
|---------------|---------------------------------------------------------|-------------------------|
| `noise_gate`  | Suppresses quiet background noise below a threshold     | `enable_noise_gate`     |
| `autotune`    | Detects pitch and snaps it to the nearest musical note  | `enable_autotune`       |
| `tone_filter` | Smooths harsh transitions for a cleaner tone            | `enable_tone_filter`    |
| `reverb`      | Adds acoustic ambience for a fuller sound               | `enable_reverb`         |

All logic is pipelined and tested using a Verilog testbench that takes `.mem` input and outputs `.mem` and pitch logs.

### 🧪 Simulation and Analysis Workflow

1. **Input WAV → .mem**: We convert `.wav` files to `.mem` (16-bit sample format) for simulation input.
2. **Verilog Testbench**: Feeds the samples through the DSP chain and outputs `processed_output.mem` and `pitch_log.csv`.
3. **.mem → WAV/Graphs**: Python tools convert `.mem` back to `.wav` and generate:
   - Waveform comparisons
   - Spectrogram visualizations
   - Frequency tracking from `pitch_log.csv`

This setup allows rapid testing without requiring real-time audio or the HPS.

### 🎼 C-Scale Simulation Comparison

We tested the DSP using a **real trumpet C scale recording** sourced from an online performance. The `.wav` was converted to `.mem` and processed through our Verilog DSP chain.

#### 🔉 Input/Output Files

- `C-Scale.mem` — Input to DSP  
- `Modified_C-Scale.mem` — Output from DSP  
- `C-Scale.wav`, `Modified_C-Scale.wav` — Playback versions for listening and graphing

#### 📊 Waveform Comparison

<img src="https://github.com/user-attachments/assets/fa7f24ec-608d-4a3f-a8f8-5049691372ad" width="100%" />

#### 🌈 Spectrogram Comparison

<img src="https://github.com/user-attachments/assets/7e00d754-f969-4565-a5f2-4182532c1f48" width="100%" />

### 🔧 RTL Design Overview

All effects are instantiated in a top-level `audio_processor` module, connected in a streaming pipeline. Each stage can be toggled using control inputs.

#### 🧩 RTL Schematic

<img src="https://github.com/user-attachments/assets/ebb8b56c-fbb5-4750-86ca-471e8a5724cb" alt="RTL Schematic of Audio Processor" width="100%" />

### 🧰 Tools and Scripts

Support tools (Python-based) help automate and visualize the pipeline:

- Convert `.wav` ↔ `.mem` (16-bit PCM)
- Plot zoomed-in waveforms and full spectrograms
- Compare tuned and detuned sine waveforms
- Log estimated vs. target pitch (`pitch_log.csv`)

### ⚙️ Current Features and Limitations

✅ Modular Verilog-based DSP design  
✅ Per-module enable control for experimentation  
✅ Accurate pitch tracking on synthetic tones  
✅ `.mem`-based simulation and conversion pipeline  
🛠️ Needs tuning of smoothing and reverb effects  
🛠️ Output distortion in some test cases under review  
🚫 Not yet integrated with real-time audio input/output or HPS


---

## 🔗 Phase 3: Integrated Audio Enhancement System (Planned)

This final phase merges Phase 1 and Phase 2 into a cohesive pipeline.

<img src="https://github.com/user-attachments/assets/711120dc-776c-41f0-a3df-b6682602bf07" alt="Integrated System Block Diagram" width="600"/>


### 🧩 Integration Goals

* Real-time audio capture and enhancement
* Seamless communication between HPS and FPGA
* Live output through codec or headphone jack
* Maybe a user interface (GUI or Web-based) for effect control

---

## ✅ Current Status

| Component                       | Status         |
| ------------------------------- | -------------- |
| Phase 1: Pitch Detection on HPS | ✅ Completed    |
| Phase 2: FPGA DSP Effects       | 🔄 In Progress |
| Phase 3: System Integration     | 🔜 Planned     |

---

## 🔭 Next Steps

* 📂 Finalize `.wav` streaming from HPS to FPGA
* 🔌 Implement AXI/FIFO audio bridge
* 🧠 Design and test FPGA DSP modules:

  * Pitch correction
  * Reverb
  * Echo suppression
* 🎧 Interface FPGA output to WM8731
* 🖥️ Build effect control interface
* 🎺 Validate system with live trumpet input
