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

def create_image(image_array, file_name):
    frame = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_name, frame)
    print("Created image!")

def on_motion(detect_func, camera):
    print("Motion detected!!!")
    camera.start(show_preview=False)
    image_name = create_file_name()
    time.sleep(1)

    image_frame = camera.capture_array()
    is_cat_detected = detect_func(image_frame)
    print(f"Is cat detected?: {is_cat_detected}")

    create_image(image_frame, image_name)

    # if(is_cat_detected):
    #     # Send image to API
    #     print("Sending image to API")
    # else:
    #     print("Doing nothing...")
    #
    time.sleep(5)

def main():
    detector = YoloDetector()
    # PIR - GPIO 4 (PIN 7)
    pir = MotionSensor(4)

    # PiCamera
    camera = Picamera2()
    camera.preview_configuration.main.size = (1280, 1280)
    camera.preview_configuration.align()
    capture_config = camera.create_still_configuration()
    camera.configure("preview")
    try:
        while True:
            print("Waiting for motion...")
            # Blocks until motion is detected
            pir.wait_for_motion()
            on_motion(detector.detect, camera)
    except KeyboardInterrupt:
        print("Stopping...")

# Only runs if this file is being ran directly in the terminal
if __name__ == "__main__":
    main()

