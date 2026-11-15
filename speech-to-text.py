from faster_whisper import WhisperModel
import os
import gc
import sys

print("Loading Whisper Model...", flush=True)
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=4)
print("Transcribing...\n", flush=True)
segments, info = model.transcribe("output.wav", beam_size=1, vad_filter=True)




with open("transcript.txt", "w", encoding="utf-8") as file:
	for segment in segments:
		line = segment.text.strip()
		print(line, flush=True)
		file.write(line + "\n")


del model
gc.collect()

os.system(f"{sys.executable} -u summariser.py")

