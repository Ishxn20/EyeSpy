import os
import sounddevice as sd
import numpy as np
import whisper
import openai
import soundfile as sf
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
openai.api_key = os.getenv("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")
# Load Whisper Model
model = whisper.load_model("base")  # Use "tiny", "base", "small", "medium", or "large"

# Set Microphone Input Device (Change device index if needed)
DEVICE_INDEX = 2  # Check your device index with `sd.query_devices()`
SAMPLE_RATE = 44100
DURATION = 10  # Record 10 seconds of audio

def record_audio(duration=DURATION, sample_rate=SAMPLE_RATE, device=DEVICE_INDEX):
    """Records audio from the microphone."""
    print("🎤 Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32, device=device)
    sd.wait()
    print("✅ Recording finished.")
    return audio

def transcribe_audio_with_timestamps(audio_file, interval=900):  # 900 sec = 15 min
    """Transcribes speech to text using Whisper with timestamps."""
    print("📝 Transcribing with timestamps...")
    whisper_result = model.transcribe(audio_file, word_timestamps=True)

    segments = whisper_result["segments"]
    transcript_with_timestamps = []
    
    for segment in segments:
        start_time = segment["start"]  # Start time in seconds
        end_time = segment["end"]  # End time in seconds
        text = segment["text"]

        # Append transcript at set intervals
        if int(start_time) % interval == 0:
            formatted_time = f"{int(start_time)//60} min {int(start_time)%60} sec"
            transcript_with_timestamps.append(f"[{formatted_time}] {text}")

    return transcript_with_timestamps

# Example usage:
# transcribed_text = transcribe_audio_with_timestamps("audio.wav")
# print("\n📝 Transcribed Text with Timestamps:\n")
# for line in transcribed_text:
#    print(line)

def process_with_gpt(transcribed_text, prompt_type="summary"):
    """🤖 Sends transcribed text to OpenAI GPT for further processing."""
    
    if prompt_type == "summary":
        prompt = f"Summarize this lecture transcript in 3 bullet points:\n\n{transcribed_text}"
    elif prompt_type == "keywords":
        prompt = f"Extract key topics and keywords from this text:\n\n{transcribed_text}"
    elif prompt_type == "translate":
        prompt = f"Translate this transcript into French:\n\n{transcribed_text}"
    else:
        prompt = transcribed_text  # Default: Just send the raw transcript to GPT

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# ✅ Step 1: Record Audio
audio_data = record_audio()

# ✅ Step 2: Save as a WAV File (Whisper requires a file input)
sf.write("audio.wav", audio_data, SAMPLE_RATE)

# ✅ Step 3: Transcribe Audio with Timestamps
transcribed_text = transcribe_audio_with_timestamps("audio.wav")
print("\n📝 Transcribed Text with Timestamps:\n")
for line in transcribed_text:
    print(line)

# ✅ Step 4: Process with GPT (Choose summary, keywords, or translation)
gpt_response = process_with_gpt("\n".join(transcribed_text), prompt_type="summary")
print("\n📌 GPT Summary:\n", gpt_response)
