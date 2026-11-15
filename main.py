import pyaudio
import wave
import keyboard
import time
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000        # Matches USB mic native hardware rate
CHUNK = 4096        # Prevents USB packet drops on Raspberry Pi
OUTPUT_FILENAME = "output.wav"
DEVICE_INDEX = 1    # Make sure this is your USB mic index

frames = []

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()

print("Press SPACE to start recording...")
keyboard.wait('space')
while keyboard.is_pressed('space'):
    time.sleep(0.01)

# Opens stream in dedicated background thread (non-blocking)
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX,
                    stream_callback=callback)

stream.start_stream()
print("Recording... Press SPACE to stop.")

keyboard.wait('space')
print("Stopping...")

stream.stop_stream()
stream.close()
audio.terminate()

with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Saved {OUTPUT_FILENAME}")

os.system("python speech-to-text.py")
