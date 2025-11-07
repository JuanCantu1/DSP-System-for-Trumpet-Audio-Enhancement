import socket
import threading
import csv
import matplotlib.pyplot as plt
import os
from main import start_recording

HOST = '0.0.0.0'
PORT = 50007

recording_thread = None
recording_data = None
recording_active = False
client_conn = None

def send_to_client(freq, concert, trumpet):
    if client_conn:
        message = f"{freq:.2f},{concert},{trumpet}\n"
        try:
            client_conn.sendall(message.encode())
        except:
            print("⚠️ Failed to send to client.")

def send_reset():
    try:
        client_conn.sendall(b"__RESET__\n")
    except:
        print("⚠️ Could not send reset message.")

def save_files(timestamps, freqs, concert_notes, trumpet_notes):
    csv_file = 'frequency_log.csv'
    png_file = 'frequency_graph.png'

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', 'Frequency (Hz)', 'Concert Note', 'Trumpet Note'])
        for t, f_, c, t_ in zip(timestamps, freqs, concert_notes, trumpet_notes):
            writer.writerow([t, f_, c, t_])

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, freqs, marker='o', linestyle='-')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Trumpet Frequency Over Time")
    plt.grid(True)
    plt.savefig(png_file)
    plt.close()

    print(f"✅ Saved {csv_file} and {png_file}")
    return csv_file, png_file

def send_file(conn, filename):
    if not os.path.exists(filename):
        print(f"⚠️ File {filename} not found.")
        return
    size = os.path.getsize(filename)
    header = f"__FILE__:{filename}:{size}\n"
    conn.sendall(header.encode())

    with open(filename, 'rb') as f:
        while chunk := f.read(1024):
            conn.sendall(chunk)
    print(f"✅ Sent file: {filename}")

def server_loop():
    global recording_thread, recording_data, recording_active, client_conn

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"📡 Server listening on port {PORT}...")

    client_conn, addr = server_socket.accept()
    print(f"🔌 Client connected from {addr}")

    def should_continue():
        return recording_active

    while True:
        cmd = input("🔧 Enter command (start / stop / send / exit): ").strip().lower()

        if cmd == "start":
            if recording_active:
                print("⚠️ Already recording.")
                continue

            send_reset()  # Instruct client to clear GUI

            def record():
                global recording_data
                recording_data = start_recording(send_func=send_to_client, should_continue=should_continue)

            recording_active = True
            recording_thread = threading.Thread(target=record)
            recording_thread.start()

        elif cmd == "stop":
            if not recording_active:
                print("⚠️ Not currently recording.")
                continue
            recording_active = False
            print("⏳ Waiting for recording to finish...")
            recording_thread.join()
            print("✅ Recording stopped.")

        elif cmd == "send":
            if not recording_data:
                print("⚠️ No data to send.")
                continue
            csv_file, png_file = save_files(*recording_data)
            send_file(client_conn, csv_file)
            send_file(client_conn, png_file)

        elif cmd == "exit":
            print("🔚 Closing connection.")
            client_conn.close()
            break

        else:
            print("❓ Unknown command. Use: start / stop / send / exit.")

    server_socket.close()

if __name__ == "__main__":
    server_loop()