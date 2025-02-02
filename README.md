# **EyeSpy**

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Object Detection System](#running-the-object-detection-system)
  - [Running the Audio Transcription System](#running-the-audio-transcription-system)
- [Implementation Details](#implementation-details)
  - [Object Detection and Video Processing](#object-detection-and-video-processing)
  - [Audio Recording and Transcription](#audio-recording-and-transcription)
- [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## **Overview**

**EyeSpy** is an **AI-powered system** that provides **real-time object detection** and **audio transcription** capabilities. 

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

---

## **Features**

### **1. Object Detection and Video Recording**
✔ **Uses SSD MobileNet v3** for real-time object detection.  
✔ **Processes a live webcam feed** to detect objects.  
✔ **Highlights detected objects** with bounding boxes & confidence scores.  
✔ **Records a 15-second video clip** when a mobile phone is detected.  
✔ **Saves videos with timestamps** for easy tracking.  
✔ **Provides a GUI for playback** of the last recorded video.  

![Object Detection Example](https://via.placeholder.com/800x400.png?text=Object+Detection+Example)  
(*Placeholder for Object Detection Image*)

---

### **2. Audio Transcription System**
✔ **Records audio continuously** in fixed intervals (default: 15 minutes).  
✔ **Uses OpenAI Whisper** for high-accuracy transcription.  
✔ **Saves transcriptions with timestamps** for easier analysis.  
✔ **Stores both `.wav` and `.txt` files** in an organized directory.  
✔ **Supports multi-language speech recognition**.  

![Audio Transcription Example](https://via.placeholder.com/800x400.png?text=Audio+Transcription+Example)  
(*Placeholder for Transcription System Image*)

---

## **Project Structure**
The project follows a **modular structure** for scalability and maintainability.

```
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

Installation

System Requirements
Operating System: Windows, macOS, or Linux
Python Version: 3.8 or later
Camera: Required for object detection
Microphone: Required for transcription system
Dependency Installation

To install the required dependencies, use the following command: pip install -r requirements.txt

Alternatively, you can install the dependencies manually using: pip install opencv-python numpy tensorflow whisper tkinter sounddevice

Usage

Running the Object Detection System
To run the system that detects mobile phones and records videos, execute: python phone_detection.py

- The webcam feed will start, and objects will be detected in real-time.
- If a mobile phone is detected, the system will start recording a 15-second video clip.
- The recorded video will be saved in the recordings/ directory with a timestamped filename.
- The GUI will provide a button to play the last recorded video.
- Press 'q' to exit the live feed.


Running the Audio Transcription System

To record and transcribe audio, execute: python audio_transcription.py

- The system will record audio in fixed intervals (e.g., 15 minutes per file).
- The recorded .wav file will be saved in the transcripts/ directory.
- The system will then use OpenAI Whisper to generate a text transcription.
- The transcribed conversation will be saved in a corresponding .txt file.

Implementation Details

Object Detection and Video Processing

- The script initializes the SSD MobileNet v3 model for detecting objects using a webcam feed.
- It reads the COCO class labels from coco.names to identify objects.
- The detection threshold is set to 50% confidence to avoid false positives.
- If a mobile phone is detected:
- A bounding box is drawn around it.
- The phone’s label and confidence score are displayed.
- A 15-second video is recorded and saved.
- The system continuously monitors the camera feed and triggers recordings as needed.

Audio Recording and Transcription
- The system records continuous audio in fixed chunks (default: 15 minutes).
- Once a recording is complete, it is saved as a .wav file in the transcripts/ folder.
- The system then uses OpenAI Whisper to process the audio.
- A text transcript is generated and saved alongside the audio file.
- Each transcript includes timestamps to indicate when certain speech occurred.

Graphical User Interface (GUI)

The system includes a Tkinter-based GUI that allows users to:

- Play the last recorded video using a simple button interface.
- Receive notifications if no video has been recorded yet.
- Easily navigate through saved recordings for analysis.

Common Issues and Troubleshooting

1. Camera Not Detected
Ensure that the webcam is properly connected.
Check the camera index in the script: cap = cv2.VideoCapture(0)  # Change 0 to 1 if using an external camera

Run the following command to check if OpenCV can access the camera: python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

2. No Phone Detected
Ensure the coco.names file is correctly loaded.
Reduce the confidence threshold in:

classIds, confs, bbox = net.detect(frame, confThreshold=0.3)
wwwwwwwwwwwwwwwwwww


3. Audio Not Recording Properly
Run the following command to check the available microphones: 
import sounddevice as sd
print(sd.query_devices())

                 
Update the script to use the correct microphone device index.

Future Enhancements

This project can be further expanded with the following features:

Automated Alerts: Send email or mobile notifications when a phone is detected.
Cloud Integration: Store recordings in Google Drive, Dropbox, or AWS S3.
Enhanced Whisper Processing: Use fine-tuned Whisper models for domain-specific accuracy.
Live Audio Translation: Translate spoken words into different languages in real-time.
Improved UI: Allow users to adjust settings such as recording duration, confidence threshold, and microphone selection.

License

This project is licensed under the MIT License.

Acknowledgments

This project utilizes the following technologies:

OpenCV for computer vision and real-time object detection.
TensorFlow Object Detection API for deep learning-based object recognition.
OpenAI Whisper for state-of-the-art speech recognition.
Tkinter for building a graphical user interface.
For more details or contributions, please reach out via email or submit an issue in the repository.

This **markdown-formatted README** provides a **comprehensive guide** to setting up, using, and expanding the system. Let me know if you need further refinements.






