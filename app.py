import sys
import wave
import time
import pyaudio
import subprocess
from flask import Flask, render_template, Response

app = Flask(__name__)

# Stores every line printed to your terminal
terminal_logs = []

class LiveTerminal:
    def __init__(self, original):
        self.original = original

    def write(self, text):
        self.original.write(text)  # Still prints in your SSH terminal
        self.original.flush()
        if text:
            terminal_logs.append(text)

    def flush(self):
        self.original.flush()

# Redirects ALL print() and error messages into terminal_logs
sys.stdout = LiveTerminal(sys.stdout)
sys.stderr = LiveTerminal(sys.stderr)

# Your exact USB mic settings:
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 4096
OUTPUT_FILENAME = "output.wav"
DEVICE_INDEX = 1

frames = []
audio = None
stream = None

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (None, pyaudio.paContinue)

@app.route("/")
def home():
    return render_template("index.html")

# Live feed endpoint that sends every new terminal character to the webpage
@app.route("/stream_logs")
def stream_logs():
    def generate():
        index = 0
        while True:
            while index < len(terminal_logs):
                chunk = terminal_logs[index]
                index += 1
                # Format newlines safely for Server-Sent Events
                safe_chunk = chunk.replace("\n", "\\n")
                yield f"data: {safe_chunk}\n\n"
            time.sleep(0.05)

    return Response(generate(), mimetype="text/event-stream")

@app.route("/start_record")
def start_record():
    global audio, stream, frames
    print("\n--- Starting Recording ---")
    frames = []
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=DEVICE_INDEX,
                        stream_callback=callback)
    stream.start_stream()
    print("Recording in progress...")
    return "Started"

@app.route("/stop_record")
def stop_record():
    global audio, stream
    if stream:
        print("Stopping recording...")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"Saved {OUTPUT_FILENAME}\n")
        stream = None
        audio = None
    return "Stopped"

@app.route("/summarise")
def summarise():
    print("--- Running speech-to-text.py ---")
    process = subprocess.Popen(
        [sys.executable, "-u", "speech-to-text.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # Reads every character from speech-to-text.py -> summariser.py into print()
    while True:
        char = process.stdout.read(1)
        if not char and process.poll() is not None:
            break
        if char:
            print(char, end="", flush=True)

    print("\n--- Finished ---\n")
    return "Done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

