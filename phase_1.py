import time
import datetime
import os
import cv2

from gpiozero import MotionSensor
from picamera2 import Picamera2
from ai_vision import YoloDetector

def create_file_name():
    images_directory = "images"
    # Creates the images directory if it's not already there
    os.makedirs(images_directory, exist_ok=True)
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
    return os.path.join(images_directory, file_name)

def create_image(image_array):
    file_name = create_file_name()
    cv2.imwrite(file_name, image_array)
    print("Created image!")

def on_motion(detect_func, camera):
    print("Motion detected!!!")
    results = detect_func(camera)
    is_cat_detected = results["is_cat_detected"]
    print(f"Is cat detected?: {is_cat_detected}")

    # Only creates image if cat is detected
    if results["is_cat_detected"]:
        create_image(results["image_frame"])
        # Sends image to AP
    time.sleep(5)

def main():
    # PIR - GPIO 4 (PIN 7)
    pir = MotionSensor(4)
    detector = YoloDetector()

    # PiCamera
    camera = Picamera2()
    camera.preview_configuration.main.size = (1280, 1280)
    camera.preview_configuration.main.format = "RGB888"
    camera.preview_configuration.align()
    camera.configure("preview")
    camera.start(show_preview=False)
    time.sleep(2)
    try:
        while True:
            print("Waiting for motion...")
            # Blocks until motion is detected
            pir.wait_for_motion()
            on_motion(detector.detect, camera)
    except KeyboardInterrupt:
        print("Stopping...")
        camera.stop()

# Only runs if this file is being ran directly in the terminal
if __name__ == "__main__":
    main()

