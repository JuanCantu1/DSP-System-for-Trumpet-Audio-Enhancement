# 🎺 FPGA-Based Digital Signal Processor for Trumpet Audio Enhancement  

### 📍 Overview
This project develops a **real-time audio enhancement system for trumpet** using the **DE1-SoC FPGA**.  
It combines **Python-based frequency detection** with **Verilog-based DSP modules** to enhance live trumpet sound in hardware.  
The system currently simulates all DSP modules in Vivado and interfaces through Python for signal analysis and audio verification.  

🎯 **Goal:** Create a modular FPGA pipeline capable of real-time **autotune, reverb, compression, noise gating, and tonal enhancement** — optimized for brass performance.  

---

### 🧩 System Architecture


<img src="https://github.com/user-attachments/assets/6254f99b-831c-4ca1-b2d7-eaa3e7d0eff9" width="100%" />


Each block can be toggled independently from the **top-level module `audio_processor.v`**, enabling flexible experimentation and effect chaining.

---

### 🎬 Demonstration

🎥 **Watch the system in action**  
📁 `Demo.mp4` — Demonstrates live pitch detection, note mapping, and real-time graphing.  
🔊 **Make sure your volume is on!**

<video src="https://github.com/user-attachments/assets/2d0dee5a-57bc-4de3-bd50-d095a3c48c55" controls width="600"></video>

---

### 🔧 Design Summary

The system is composed of modular **Verilog DSP blocks** and a **Python-based front end** for preprocessing and analysis.  
The FPGA operates entirely in fixed-point arithmetic, streaming one 16-bit audio sample per clock cycle.  

| Module | Description | Control Signal |
|---------|-------------|----------------|
| `noise_gate` | Suppresses background noise below threshold | `enable_noise_gate` |
| `autotune` | Detects pitch and corrects to nearest musical note | `enable_autotune` |
| `tone_filter` | Smooths transitions, reduces harsh tones | `enable_tone_filter` |
| `reverb` | Adds room ambience and spatial depth | `enable_reverb` |
| `compressor` | Balances dynamic range of performance | `enable_compressor` |
| `resonator` | Adds formant resonance to enhance brightness | `enable_resonator` |
| `trumpet_warmer` | Adds analog-style harmonic warmth | `enable_warmer` |
| `harmonic_exciter` | Restores lost overtones in filtered signals | `enable_exciter` |

Each module has adjustable parameters (thresholds, hold times, gain factors, mix ratios), allowing easy customization.

---

### 🧠 Simulation and Analysis Workflow

1. **Audio Preprocessing (Python)**
   - Convert `.wav` → `.mem` for Verilog simulation.  
   - Normalize amplitudes and segment test samples.  

2. **FPGA Simulation (Vivado XSIM)**
   - Feed `.mem` vectors into `audio_tb.v`.  
   - Enable or disable modules via control signals.  
   - Output processed audio as `.mem`.  

3. **Post-Processing (Python)**
   - Convert `.mem` → `.wav` for playback.  
   - Plot waveform and spectrogram comparisons.  

---

### 🎧 Example: Trumpet C Scale Processing

A real trumpet **C scale recording** was used as a test case for pipeline validation.  
Below are waveform and spectrogram comparisons before and after DSP processing.

#### 📉 Waveform Comparison
<img src="https://github.com/user-attachments/assets/fa7f24ec-608d-4a3f-a8f8-5049691372ad" width="100%" />

#### 🌈 Spectrogram Comparison
<img src="https://github.com/user-attachments/assets/7e00d754-f969-4565-a5f2-4182532c1f48" width="100%" />

---

### 🔩 RTL Architecture

<img src="https://github.com/user-attachments/assets/59f2b523-6b8e-4c30-9338-7af8ab971773" alt="RTL Schematic of Audio Processor" width="100%" />

Each module is instantiated within the top-level `audio_processor.v` as a **streaming DSP chain**, operating at 48 kHz sample rate.  
Simulation results confirm sub-15 ms latency across the entire path, suitable for real-time performance.

---

### 🧰 Development Environment

| Domain | Tools / Frameworks |
|--------|---------------------|
| FPGA Design | Verilog, Vivado 2023.1, Quartus (DE1-SoC) |
| Audio Processing | Python, NumPy, Librosa, Matplotlib |
| Conversion Tools | Custom `.wav ↔ .mem` converters |
| Simulation | Vivado XSIM testbench (`audio_tb.v`) |
| Platform | Cyclone V SoC with WM8731 audio codec |

---

### ⚙️ Parameters and Tuning

| Parameter | Description | Typical Range |
|------------|-------------|----------------|
| `THRESHOLD` | Noise gate level | 100 – 2000 |
| `MIX_SHIFT` | Reverb/Tone mix coefficient | 0 – 15 |
| `FRAME_SIZE` | Autotune window | 512 – 2048 |
| `SAMPLE_RATE` | Audio sample rate | 48 000 Hz |
| `HOLD_TIME` | Noise gate release cycles | 5 – 15 |

---

### 🧪 Performance Goals & Target Metrics

| **Metric** | **Target / Goal** | **Description** |
|-------------|-------------------|-----------------|
| **Latency** | < 15 ms end-to-end | Maintain imperceptible delay for real-time playability in live trumpet performance. |
| **SNR (Signal-to-Noise Ratio)** | > 60 dB | Achieve clean output with effective noise gating and dynamic range compression. |
| **Pitch Accuracy** | ±1 semitone | Autotune should stabilize pitch within one semitone of target note for live input. |
| **Fixed-Point Precision** | 16-bit | Maintain high-quality DSP processing using resource-efficient arithmetic. |
| **Resource Utilization** | < 70 % LUT, < 60 % FF | Ensure design fits comfortably within Cyclone V FPGA fabric for real-time operation. |
| **Sample Rate** | 48 kHz | Match standard audio rate for compatibility with WM8731 codec and real-time systems. |
| **System Throughput** | 1 sample/clk | Fully pipelined design enabling continuous audio streaming without stalls. |


---

### 📂 Repository Structure

```
fpga-trumpet-dsp/
├─ verilog/
│  ├─ src/        # All DSP modules and audio_processor.sv (stubs included)
│  └─ sim/        # audio_tb.sv and tiny .mem stimulus
├─ python/
│  ├─ io/         # wav_to_mem.py, mem_to_wav.py
│  ├─ analysis/   # waveform/spectrogram & comparison scripts
│  └─ synth/      # sine + scale generators
├─ iot-frequency/ # client/server placeholders + README
├─ docs/          # put your draw.io export + Vivado RTL screenshot here
├─ media/         # Demo video + images for README
├─ .gitignore     # Vivado/Python/audio artifacts ignored
└─ LICENSE        # MIT

```

---

### 📡 IoT Frequency Analysis (Companion Project)
A complementary Python system for real-time frequency detection, TCP/IP data logging, and visualization.  
Originally built as the prototype for HPS-side pitch tracking, now used as a front-end analysis tool.  

📄 See: `IoT Final Project/IoT_Frequency_Analysis_System_for_Musical_Instruments.pdf`

---

### 🧭 Future Improvements
- Replace zero-crossing pitch detection with **AMDF/YIN** for robustness.  
- Integrate live audio I/O via **WM8731 codec** on DE1-SoC.  
- Real-time visualization through **HPS-to-FPGA bridge**.  
- Hardware resource profiling and fixed-point optimization.  

---

### 📚 Technologies
`Verilog` · `Python` · `Vivado` · `NumPy` · `Librosa` · `Cyclone V FPGA` · `Audio DSP` · `Embedded Systems`

---

### 📜 License
MIT License — open for academic, educational, and research use.
