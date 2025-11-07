import socket
import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import os

SERVER_IP = '192.168.0.37'  # Replace with your server's IP
PORT = 50007

time_data = []
frequency_data = []
max_duration = 60  # Show last 60 seconds

class FrequencyClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎺 Trumpet Pitch Monitor")

        self.file_counter = 1

        # === UI Layout ===
        self.label_frame = ttk.LabelFrame(root, text="Live Pitch Data", padding=10)
        self.label_frame.pack(fill='x', padx=10, pady=10)

        self.freq_label = ttk.Label(self.label_frame, text="Frequency: -- Hz", font=("Arial", 14))
        self.freq_label.pack(pady=5)

        self.concert_label = ttk.Label(self.label_frame, text="Concert Note: --", font=("Arial", 14))
        self.concert_label.pack(pady=5)

        self.trumpet_label = ttk.Label(self.label_frame, text="Trumpet Note: --", font=("Arial", 14))
        self.trumpet_label.pack(pady=5)

        # === Matplotlib Plot ===
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.line, = self.ax.plot([], [], marker='o')
        self.ax.set_title("Live Frequency Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Frequency (Hz)")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        self.start_time = time.time()

        threading.Thread(target=self.start_client, daemon=True).start()
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=500)

    def reset_gui(self):
        print("🔁 Resetting GUI...")
        global time_data, frequency_data
        time_data.clear()
        frequency_data.clear()
        self.start_time = time.time()

        self.freq_label.config(text="Frequency: -- Hz")
        self.concert_label.config(text="Concert Note: --")
        self.trumpet_label.config(text="Trumpet Note: --")

        self.update_plot(None)

    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, PORT))
            print("Connected to server.")

            buffer = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                buffer += data

                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    decoded = line.decode(errors="ignore").strip()

                    if decoded == "__RESET__":
                        self.reset_gui()

                    elif decoded.startswith("__FILE__"):
                        _, fname, fsize = decoded.split(":")
                        fsize = int(fsize)
                        base_fname = os.path.basename(fname)
                        name, ext = os.path.splitext(base_fname)
                        numbered_fname = f"client_{name}_{self.file_counter}{ext}"
                        self.file_counter += 1

                        print(f"📥 Receiving file: {base_fname} ({fsize} bytes)")
                        with open(numbered_fname, 'wb') as f:
                            received = 0
                            while received < fsize:
                                chunk = client_socket.recv(min(1024, fsize - received))
                                if not chunk:
                                    break
                                f.write(chunk)
                                received += len(chunk)
                        print(f"✅ File saved as {numbered_fname}")
                        msgbox.showinfo("File Received", f"File saved: {numbered_fname}")

                    else:
                        parts = decoded.strip().split(',')
                        if len(parts) == 3:
                            freq, concert, trumpet = parts
                            self.update_ui(freq, concert, trumpet)

    def update_ui(self, freq, concert, trumpet):
        self.freq_label.config(text=f"Frequency: {freq} Hz")
        self.concert_label.config(text=f"Concert Note: {concert}")
        self.trumpet_label.config(text=f"Trumpet Note: {trumpet}")

        try:
            timestamp = round(time.time() - self.start_time, 1)
            freq_val = float(freq)
            time_data.append(timestamp)
            frequency_data.append(freq_val)

            while time_data and (time_data[-1] - time_data[0]) > max_duration:
                time_data.pop(0)
                frequency_data.pop(0)

        except ValueError:
            pass

    def update_plot(self, _):
        self.line.set_data(time_data, frequency_data)
        if time_data:
            self.ax.set_xlim(time_data[0], time_data[-1])
            ymin = min(frequency_data) - 10
            ymax = max(frequency_data) + 10
            self.ax.set_ylim(ymin, ymax)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FrequencyClientGUI(root)
    root.mainloop()