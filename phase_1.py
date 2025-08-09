import time
import datetime
import os
import cv2
import asyncio

from gpiozero import MotionSensor
from picamera2 import Picamera2
from ai_vision import YoloDetector
from telegram_bot import CatSecurityBot

def create_file_name():
    """Creates a filename for an image that includes date and time and returns a images/create_file_name.jpg path"""
    images_directory = "images"
    # Creates the images directory if it's not already there
    os.makedirs(images_directory, exist_ok=True)
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
    return os.path.join(images_directory, file_name)

def create_image(image_array) -> str:
    file_name = create_file_name()
    cv2.imwrite(file_name, image_array)
    print("Created image!")
    return file_name


MOTION_SLEEP_DELAY = 5
async def on_motion(detect_func, camera, bot) -> None:
    print("Motion detected!!!")
    results = detect_func(camera)
    is_cat_detected = results["is_cat_detected"]
    print(f"Is cat detected?: {is_cat_detected}")

    # Only creates image if cat is detected
    if results["is_cat_detected"]:
        image_path = create_image(results["image_frame"])
        await bot.send_image(image_path, "Cat detected")
    await asyncio.sleep(MOTION_SLEEP_DELAY)

async def main():
    # PIR - GPIO 4 (PIN 7)
    pir = MotionSensor(4)
    detector = YoloDetector()
    bot = CatSecurityBot()

    # PiCamera
    camera = Picamera2()
    camera.preview_configuration.main.size = (1280, 1280)
    camera.preview_configuration.main.format = "RGB888"
    camera.preview_configuration.align()
    camera.configure("preview")
    camera.start(show_preview=False)
    await asyncio.sleep(3)

    try:
        while True:
            print("Waiting for motion...")
            # Blocks until motion is detected
            await asyncio.to_thread(pir.wait_for_active)
            await on_motion(detector.detect, camera, bot)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        camera.stop()
        await bot.shutdown()
        print("Camera stopped.")
# Only runs if this file is being ran directly in the terminal
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited by user")

