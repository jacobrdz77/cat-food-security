from gpiozero import MotionSensor
from picamera2 import Picamera2
import time
import datetime
import os

# PIR - GPIO 4 (PIN 7)
pir = MotionSensor(4)

# PiCamera
camera = Picamera2()
camera.preview_configuration.main.size = (1280, 1280)
camera.preview_configuration.align()
capture_config = camera.create_still_configuration()
camera.configure("preview")

def create_file_name():
    images_directory = "images"
    # Creates the images directory if it's not already there
    os.makedirs(images_directory, exist_ok=True)
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.jpg")

    return os.path.join(images_directory, file_name)

def on_motion():
    print("Motion detected!!!")
    camera.start(show_preview=True)
    image_name = create_file_name()
    time.sleep(.2)
    camera.switch_mode_and_capture_file(capture_config, image_name)
    camera.stop_preview()
    print("Saved image!")
    time.sleep(5)

def main():
    try:
        while True:
            print("Waiting for motion...")
            pir.wait_for_motion()
            on_motion()
    except KeyboardInterrupt:
        print("Stopping...")

main()

