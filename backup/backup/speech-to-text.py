from faster_whisper import WhisperModel
import os
import gc

model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=4)
print("Model loaded!")
print("Transcribing...")
segments, info = model.transcribe("output.wav", beam_size=1, vad_filter=True)




with open("transcript.txt", "w", encoding="utf-8") as file:
	for segment in segments:
		file.write(segment.text.strip() + "\n")


del model
gc.collect()

os.system("sudo -E $(which python) summariser.py")
