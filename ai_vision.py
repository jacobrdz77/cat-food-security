import threading
import cv2
import os
import datetime

from picamera2 import Picamera2
from ultralytics import YOLO
from time import sleep

stop_event = threading.Event()

def countdown(seconds):
    for i in range(seconds, 0, -1):
        if stop_event.is_set():
            return
        print(f"Countdown: {i}")
        sleep(1)
    stop_event.set()

def create_debug_name():
    images_directory = "images"
    # Creates the images directory if it's not already there
    os.makedirs(images_directory, exist_ok=True)
    debug_name = f"debug_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    return os.path.join(images_directory, debug_name)

class YoloDetector():
    """
    YoloDetector - Uses Picamera2 & Yolo model to detect objects
    """
    # ID 15 for Cat
    def __init__(self, specific_model="yolov8n_ncnn_model"):
        self.model = YOLO(specific_model, task="detect")

    # image_frame has to come from Picamera2.capture_array()
    def detect(self, picamera2):
        print("Starting detection...")
        stop_event.clear()

        # Starts 10 second timer
        countdown_thread = threading.Thread(target=countdown, args=(5,), daemon=True)
        countdown_thread.start()

        while not stop_event.is_set():
            # Run YOLO model on the captured frame and store the results
            frame = picamera2.capture_array()
            results = self.model(frame)

            detected_list = results[0].boxes.cls.tolist()
            confidence = results[0].boxes.conf.tolist()

            # print(f"Detected IDs: {detected_list}")
            # print(f"Confidence: {confidence}")

            for i, obj_id in enumerate(detected_list):
                # print(f"ID: {obj_id}")
                if obj_id == 15 :
                    print("Cat detected!")
                    print(f"Confidence of CAT: {confidence[i]} ")

                    # confidence has to be greater than 65% to be considered a cat
                    if confidence[i] < 0.65:
                        print("*****Not CAT enough! Continuing...******")
                        continue

                    stop_event.set()
                    countdown_thread.join()
                    # Send message to API with image attached
                    return {"is_cat_detected": True, "image_frame": frame} 
                if obj_id == 0:
                    print("HUMAN detected!")
                elif not detected_list:
                    print("Nothing detected...")
                    # Note: For debugging purposes
                    # debug_name = create_debug_name()
                    # cv2.imwrite(debug_name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                else:
                    print("Unknown detected!")

        countdown_thread.join()
        return {"is_cat_detected": False, "image_frame": None} 
