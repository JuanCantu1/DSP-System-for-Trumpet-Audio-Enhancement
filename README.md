# 🎺 FPGA-Based Digital Signal Processor for Trumpet Audio Enhancement

## 📌 Overview

This project aims to build a real-time **audio enhancement system for trumpet** using an FPGA platform (DE1-SoC). It is structured in two phases:

1. **Phase 1 – Pitch Detection System** ✅ *(Completed)*
   A real-time frequency detection and note-mapping system using Python and IoT concepts to analyze trumpet audio.

2. **Phase 2 – FPGA-Based DSP Effects** 🔄 *(In Progress)*
   Real-time digital signal processing using Verilog on the DE1-SoC board, targeting effects like **reverb**, **echo removal**, and **pitch correction**.

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

> 🔗 This phase is developed as a standalone Python-based client-server system.
> 📂 See: `IoT Frequency Analysis System/`

---

## 🔧 Phase 2: Real-Time DSP on FPGA (Upcoming)

This phase transitions the system from software-based analysis to **hardware-accelerated audio processing** using the DE1-SoC platform. The design leverages both the ARM processor (HPS) and the FPGA fabric in a coordinated pipeline.

### 🔁 System Architecture

> The **ARM processor** captures or receives `.wav` audio and streams it to the **FPGA**, which applies digital signal processing (DSP) effects in real time and returns the enhanced output.

**Responsibilities:**

* **HPS (ARM Cortex-A9)**

  * Handles `.wav` file I/O and audio stream capture
  * Manages protocol interfaces (e.g., AXI, DMA, or FIFO)
  * Initiates and monitors FPGA processing

* **FPGA (Cyclone V)**

  * Executes DSP effects in parallel, with low-latency hardware logic
  * Processes audio in real time via AXI/Avalon interfaces
  * Outputs enhanced audio to codec or back to HPS

### 🎧 Planned DSP Modules (Implemented on FPGA)

* **🎤 Reverb**: Simulates acoustic reflections for natural resonance
* **🔇 Echo Removal**: Suppresses delayed audio artifacts
* **🎵 Pitch Correction**: Fine-tunes inaccuracies in trumpet pitch

### 🧱 Hardware Stack

* **Board**: DE1-SoC (Cyclone V SoC FPGA + ARM Cortex-A9)
* **Audio Codec**: WM8731 (connected via I²S)
* **Audio Format**: `.wav` (uncompressed, 16-bit PCM)
* **Communication Protocol**: AXI Stream or Avalon ST between HPS and FPGA
* **Target Latency**: <15 ms total (input to output)

---

## ✅ Current Status

| Component                        | Status         |
| -------------------------------- | -------------- |
| Audio Input (Microphone, Python) | ✅ Completed    |
| Pitch Detection + Note Mapping   | ✅ Completed    |
| Frequency Graph + CSV Output     | ✅ Completed    |
| Client-Server Communication      | ✅ Completed    |
| HPS `.wav` Capture + Transfer    | 🔄 In Progress |
| FPGA DSP Effects (Verilog)       | 🔄 In Progress |

---

## 🔭 Next Steps

* 📂 Implement `.wav` file or audio stream handling on HPS
* 🔌 Develop AXI or FIFO-based audio interface from HPS to FPGA
* 🧠 Design and test Verilog DSP modules for:

  * Pitch correction
  * Reverb
  * Echo suppression
* 🎧 Interface processed audio with WM8731 codec for playback
* 📡 Prototype optional web/mobile control dashboard
* 🎺 Test full pipeline with live trumpet input
