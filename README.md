# **EyeSpy: AI-Powered Object Detection & Audio Transcription System**

## **Overview**

EyeSpy is an **AI-powered system** that provides **real-time object detection** and **audio transcription** capabilities.

This system:
- Detects **mobile phones and other objects** using a **live video stream**.
- **Records video** when a phone is detected and timestamps the event.
- Provides a **Graphical User Interface (GUI)** to review recorded videos.
- Offers an **alternative version** that captures **audio recordings** and transcribes speech using **OpenAI Whisper**.

### **Technology Stack**

- **Computer Vision:** OpenCV, TensorFlow Object Detection API
- **Speech-to-Text:** OpenAI Whisper
- **GUI Interface:** Tkinter
- **Audio Processing:** Sounddevice, Numpy

## **Features**

### **1. Object Detection and Video Recording**

- **Uses SSD MobileNet v3** for real-time object detection.
- **Processes a live webcam feed** to detect objects.
- **Highlights detected objects** with bounding boxes & confidence scores.
- **Records a 15-second video clip** when a mobile phone is detected.
- **Saves videos with timestamps** for easy tracking.
- **Provides a GUI for playback** of the last recorded video.

![Object Detection Example](https://via.placeholder.com/800x400.png?text=Object+Detection+Example)  
(*Placeholder for Object Detection Image*)

### **2. Audio Transcription System**

- **Records audio continuously** in fixed intervals (default: 15 minutes).
- **Uses OpenAI Whisper** for high-accuracy transcription.
- **Saves transcriptions with timestamps** for easier analysis.
- **Stores both `.wav` and `.txt` files** in an organized directory.
- **Supports multi-language speech recognition**.

![Audio Transcription Example](https://via.placeholder.com/800x400.png?text=Audio+Transcription+Example)  
(*Placeholder for Transcription System Image*)

## **Project Structure**

The project follows a **modular structure** for scalability and maintainability.

```bash
EyeSpy/
│── README.md                  # Project documentation
│── requirements.txt            # List of required dependencies
│── phone_detection.py          # Main script for phone detection
│── audio_transcription.py      # Script for audio recording & transcription
│── Object_Detection_Files/     # Model files for object detection
│   ├── coco.names              # Object class labels
│   ├── ssd_mobilenet_v3.pbtxt  # Model configuration file
│   ├── frozen_inference_graph.pb # Pre-trained model weights
│── recordings/                 # Directory for recorded videos
│   ├── phone_detected_YYYYMMDD_HHMMSS.avi
│── transcripts/                # Directory for audio transcriptions
│   ├── conversation_YYYYMMDD_HHMMSS.txt
│   ├── conversation_YYYYMMDD_HHMMSS.wav
│── gui/                        # GUI-related files
│── logs/                       # Stores logs of detections & errors
```

## **Installation**

## System Requirements

Operating System: Windows, macOS, or Linux
Python Version: 3.8 or later
Camera: Required for object detection
Microphone: Required for transcription system
Dependency Installation

To install the required dependencies, use: ```pip install -r requirements.txt```

Alternatively, install them manually: ```pip install opencv-python numpy tensorflow whisper tkinter sounddevice```

## Usage
Running the Object Detection System
To run the system that detects mobile phones and records videos: ```python phone_detection.py```

- Live webcam feed will start, detecting objects in real-time.
- If a mobile phone is detected, a 15-second video clip is recorded.
- Recorded videos are saved in the recordings/ directory.
- The GUI allows playback of the last recorded video.
- Press 'q' to exit the live feed.
- Running the Audio Transcription System

To record and transcribe audio: ``` python audio_transcription.py```

The system will record audio in fixed intervals (default: 15 minutes).
Recorded .wav files are saved in the transcripts/ directory.
The system then uses OpenAI Whisper to generate transcriptions.
Transcribed text is saved in a .txt file alongside the audio.

## Implementation Details

Object Detection and Video Processing

- Initializes SSD MobileNet v3 to detect objects in real-time.
- Reads COCO class labels from coco.names.
- Sets a detection threshold of 50% confidence to reduce false positives.
- If a mobile phone is detected:
- A bounding box is drawn.
- The phone’s label and confidence score are displayed.
- A 15-second video is recorded and saved.
- Audio Recording and Transcription
- Records continuous audio in fixed chunks (default: 15 minutes).
- Once recording is complete, it is saved as a .wav file.
- Uses OpenAI Whisper to process the audio and generate a text transcript.
- Each transcript includes timestamps for easy reference.

## Graphical User Interface (GUI)

The system includes a Tkinter-based GUI that allows users to:

- Play the last recorded video using a simple button.
- Receive notifications if no video is available.
- Easily navigate through saved recordings.

## Common Issues and Troubleshooting

1. Camera Not Detected
Ensure that the webcam is properly connected.

Run: ```python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"```
If it returns False, change the camera index: ```cap = cv2.VideoCapture(1)  # Try 1 instead of 0```

2. No Phone Detected
Ensure coco.names is loaded correctly.
Lower the detection confidence threshold: ```classIds, confs, bbox = net.detect(frame, confThreshold=0.3)```

3. Audio Not Recording Properly
Check available microphones: ``` import sounddevice as sd
print(sd.query_devices())```

Update the script to use the correct microphone device index.

##Future Enhancements

This project can be expanded with:

- Automated Alerts: Send email or mobile notifications when a phone is detected.
- Cloud Integration: Store recordings in Google Drive, Dropbox, or AWS S3.
- Enhanced Whisper Processing: Use fine-tuned models for better accuracy.
- Live Audio Translation: Convert spoken words into different languages in real-time.
- Improved UI: Adjustable settings for recording duration, confidence threshold, and microphone selection.

## License

This project is licensed under the MIT License.

## Acknowledgments

This project utilizes:

- OpenCV for computer vision and real-time object detection.
- TensorFlow Object Detection API for deep learning-based object recognition.
- OpenAI Whisper for state-of-the-art speech recognition.
- Tkinter for building a graphical user interface.
- For contributions or support, please submit an issue in the repository.

