import os
import sounddevice as sd
import numpy as np
import whisper
import openai
import soundfile as sf
import time
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load API key securely
load_dotenv()
openai_api_key = os.getenv("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")

client = OpenAI(api_key=openai_api_key)

# ✅ Load Whisper Model
model = whisper.load_model("base")  # Use "tiny", "base", "small", "medium", "large"

# ✅ Recording settings
DEVICE_INDEX = 0  # Change based on `sd.query_devices()`
SAMPLE_RATE = 44100
CHUNK_DURATION = 60 * 5  # 300 minutes in seconds
OUTPUT_DIR = "recordings"  # Folder to save audio & transcripts
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

def record_audio(filename, duration=CHUNK_DURATION, sample_rate=SAMPLE_RATE, device=DEVICE_INDEX):
    """Records audio and saves it as a WAV file."""
    print(f"🎤 Recording {duration // 60} minutes of audio...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32, device=device)
    sd.wait()
    sf.write(filename, audio, sample_rate)
    print(f"✅ Saved recording to {filename}")

def transcribe_audio(audio_file):
    """Transcribes audio using Whisper and returns the transcript with timestamps."""
    print("📝 Transcribing with timestamps...")
    whisper_result = model.transcribe(audio_file, word_timestamps=True)

    segments = whisper_result["segments"]
    transcript_with_timestamps = []
    
    for segment in segments:
        start_time = segment["start"]
        formatted_time = f"[{int(start_time) // 60} min {int(start_time) % 60} sec]"
        text = segment["text"]
        transcript_with_timestamps.append(f"{formatted_time} {text}")

    return "\n".join(transcript_with_timestamps)

def summarize_with_gpt(transcribed_text):
    """Generates a summary with timestamps using OpenAI GPT."""
    prompt = f"Summarize this conversation with timestamps:\n\n{transcribed_text}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ✅ Loop: Automatically record, transcribe, and summarize every 15 minutes
while True:
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    audio_filename = os.path.join(OUTPUT_DIR, f"conversation_{timestamp}.wav")
    transcript_filename = os.path.join(OUTPUT_DIR, f"transcription_{timestamp}.txt")
    summary_filename = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.txt")

    # Step 1: Record Audio
    record_audio(audio_filename)

    # Step 2: Transcribe Audio
    transcribed_text = transcribe_audio(audio_filename)

    # Step 3: Save Transcription
    with open(transcript_filename, "w") as f:
        f.write(transcribed_text)
    
    print(f"✅ Transcription saved to {transcript_filename}")

    # Step 4: Generate Summary
    summary = summarize_with_gpt(transcribed_text)

    # Step 5: Save Summary
    with open(summary_filename, "w") as f:
        f.write(summary)

    print(f"✅ Summary saved to {summary_filename}")

    # ✅ Wait for the next recording cycle (15 minutes)
    print("⏳ Waiting for the next recording cycle...")
    time.sleep(CHUNK_DURATION)

