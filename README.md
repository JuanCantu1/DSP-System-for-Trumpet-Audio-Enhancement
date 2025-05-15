# 🎺 FPGA-Based Digital Signal Processor for Trumpet Audio Enhancement

## 📌 Overview

This project is an FPGA-based real-time digital signal processing (DSP) system aimed at enhancing trumpet audio. It is divided into two phases:

1. **Phase 1 – Frequency Detection (Current Subproject)**
   A system for real-time pitch detection from trumpet audio, using microphones and signal processing in Python. It validates pitch extraction accuracy before DSP effects are implemented.

2. **Phase 2 – Audio Enhancement on FPGA**
   The ultimate goal is to implement real-time DSP effects — such as **reverb**, **echo removal**, and **pitch correction** — using Verilog on a DE1-SoC board with the WM8731 audio codec.

---

## 📡 Current Subproject: Real-Time Trumpet Pitch Detection

This phase establishes the foundation for musical signal processing by capturing, analyzing, and logging the pitch of trumpet sounds in real time.

### 🎯 Goals

* Capture trumpet audio using a microphone.
* Use Python (`librosa`, `sounddevice`, `scipy`) to extract the **fundamental frequency** using the **YIN algorithm**.
* Identify corresponding **concert** and **trumpet transposed** notes.
* Store and analyze results with statistical methods (mean, standard deviation, 95% CI).
* Visualize frequency data and annotate musical notes.

### 🧪 Testing Script Summary

This script:

* Records audio samples.
* Extracts and logs frequencies.
* Maps frequencies to musical notes (concert and Bb trumpet).
* Saves results as CSV and annotated frequency graph.

> 📂 Output files:
>
> * `frequency_log.csv`: Tabulated frequency and note data
> * `frequency_graph.png`: Visual summary with annotated pitch labels

### 📈 Example Output (for G4)

> * Mean Frequency: 391.6 Hz
> * Standard Deviation: 1.8 Hz
> * 95% Confidence Interval: \[390.76, 392.44] Hz
> * Output transmitted via TCP/IP for remote monitoring

---

## 🧠 Research Context

This project is inspired by the paper:

> **"IoT-Based Real-Time Frequency Detection for Brass Instruments" – Juan Cantu**
> Uses FFT to extract trumpet frequencies and transmit them over a network using DE1-SoC and ARM HPS.

Key Takeaways:

* Demonstrated IoT integration with audio frequency analysis.
* Confirmed statistical consistency of real trumpet note detection.
* Established a scalable architecture for future DSP modules.

---

## 🔧 Project Architecture (Phase 2 Preview)

Planned enhancements to be implemented on the FPGA include:

* **Reverb**: Simulates natural acoustics of performance spaces.
* **Echo Removal**: Filters reflected or delayed signals for clarity.
* **Pitch Correction**: Adjusts slight inaccuracies in real time.

**Hardware Platform**: DE1-SoC
**Audio Interface**: WM8731 Codec
**Target Latency**: <15 ms end-to-end

---

## ✅ Status

| Component                    | Status         |
| ---------------------------- | -------------- |
| Audio Input via Microphone   | ✅ Completed    |
| Pitch Detection (Python)     | ✅ Completed    |
| Confidence Interval Analysis | ✅ Completed    |
| DE1-SoC Integration (I/O)    | 🔄 In Progress |
| Real-Time DSP Effects        | 🔜 Planned     |

---

## 🔭 Future Work

* Port Python frequency detection to DE1-SoC using C.
* Implement real-time pitch correction in Verilog.
* Integrate reverb and echo removal.
* Design mobile/web dashboards for remote feedback.
* Test in live settings with continuous input.

---
