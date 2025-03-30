import os
import sounddevice as sd
import numpy as np
import whisper
import openai
import soundfile as sf
import time
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")  # Store your key in .env
client = openai.OpenAI(api_key=openai_api_key)


DEVICE_INDEX = 1  # Change this to your microphone index
SAMPLE_RATE = 44100
CHUNK_DURATION = 60 * 5  # 5 minutes (adjust as needed)
OUTPUT_DIR = "recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)  


model = whisper.load_model("base")  #

def record_audio(filename, duration=CHUNK_DURATION, sample_rate=SAMPLE_RATE, device=DEVICE_INDEX):
    """Records audio using HW 485 microphone and saves as a WAV file."""
    print(f" Recording {duration // 60} minutes of audio from device {device}...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32, device=device)
    sd.wait()
    sf.write(filename, audio, sample_rate)


def transcribe_audio(audio_file):

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

    prompt = f"Summarize this conversation with timestamps:\n\n{transcribed_text}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


while True:
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    audio_filename = os.path.join(OUTPUT_DIR, f"conversation_{timestamp}.wav")
    transcript_filename = os.path.join(OUTPUT_DIR, f"transcription_{timestamp}.txt")
    summary_filename = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.txt")


    record_audio(audio_filename)


    transcribed_text = transcribe_audio(audio_filename)


    with open(transcript_filename, "w") as f:
        f.write(transcribed_text)
    
    print(f"✅ Transcription saved to {transcript_filename}")


    summary = summarize_with_gpt(transcribed_text)


    with open(summary_filename, "w") as f:
        f.write(summary)

    print(f"✅ Summary saved to {summary_filename}")


    print("Waiting for the next recording cycle...")
    time.sleep(CHUNK_DURATION)
