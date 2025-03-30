import cv2
import time
import datetime
import os
import threading
import tkinter as tk
from tkinter import messagebox
import subprocess


classFile = "/home/vaibhav/Desktop/Object_Detection_Files/coco.names"
configPath = "/home/vaibhav/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/vaibhav/Desktop/Object_Detection_Files/frozen_inference_graph.pb"


with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")


net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
clip_duration = 15  # seconds
last_video_path = None  # Store the last recorded video



def detect_and_draw_boxes(frame):
    classIds, confs, bbox = net.detect(frame, confThreshold=0.5)
    detected_phone = False  # Track if phone is detected

    if len(classIds) > 0:  # Ensure we have detections
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]  # Adjust index for zero-based indexing
            color = (0, 255, 0)  # Green bounding box


            if className == 'cell phone':
                detected_phone = True


            confidence_value = float(confidence)  # Convert to a float before rounding
            label = f"{className.upper()} {round(confidence_value * 100, 1)}%"
            cv2.rectangle(frame, box, color, thickness=2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return detected_phone, frame



def record_video():
    global last_video_path  # Ensure the variable updates correctly
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"phone_detected_{timestamp}.avi"
    last_video_path = video_filename  # ✅ Update the last recorded video every time a new one is made
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while time.time() - start_time < clip_duration:
        ret, frame = cap.read()
        if not ret:
            break


        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        out.write(frame)
        cv2.imshow('Recording...', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    print(f"📁 Video saved as: {video_filename}")



def run_camera():
    global last_video_path  # Ensure we access the latest video path
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected_phone, frame = detect_and_draw_boxes(frame)


        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)


        if detected_phone:
            print("📲 Phone detected! Recording video...")
            record_video()


        cv2.imshow('Live Detection', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def play_last_video():
    global last_video_path
    if last_video_path and os.path.exists(last_video_path):
        print(f"▶️ Playing: {last_video_path}")
        subprocess.run(["xdg-open", last_video_path])  # Works on Linux
    else:
        messagebox.showinfo("No Video Found", "No phone detection video recorded yet!")



def start_gui():
    root = tk.Tk()
    root.title("Phone Tracker")


    btn_play = tk.Button(root, text="Show Last Video", command=play_last_video, font=("Arial", 14))
    btn_play.pack(pady=20)

    root.mainloop()



threading.Thread(target=run_camera, daemon=True).start()


start_gui()
