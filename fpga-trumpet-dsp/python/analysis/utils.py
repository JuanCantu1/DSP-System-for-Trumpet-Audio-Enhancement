import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pitch_log.csv")
plt.plot(df["frame_num"], df["estimated_freq"])
plt.xlabel("Frame")
plt.ylabel("Frequency (Hz)")
plt.title("Estimated Pitch Over Time")
plt.grid()
plt.show()
