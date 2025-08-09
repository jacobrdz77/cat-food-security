# Cat Food Security Project

## Overview

### Current Features (Phase 1)
- ***Motion detection***: PIR sensor detects motion near the cat bowl, which then triggers the YOLO model (with camera) to run.
- ***Camera detection***: Pi Camera detects objects using the YOLO 8n model (NCNN format)
- ***Telegram Notification***: Telegram sends an image of the cat detected with a caption to the a message thread.

### Planned Features
- ***Phase 2: Auto Feeder***:
    - Using a weight sensor, it automatically adds food to the bowl when the weight is near empty weight.
    - Uses a DC motor to rotate a 3D printed auger conveyor. 

- ***Phase 3: Security***: 
    - Activate a scare mechansim (stepper motor or linear actuator).
    - Sends a telegram notification of the intruder.
    - Possible web app of recent photos and logs of detections.

## Hardware Requirements
- Raspberry Pi 5
- Raspberry Pi Camera 3
- MicroSD Card (with Raspberry Pi OS)
- Power Supply (45W USB-C for Raspberry Pi 5)
- PIR Sensor (HC-SR501)
- (Planned) Load Cell Weight Sensor (50kg with HX711), DC Motor (N20), Motor Driver (L298N), 3D Printer Filament 

## Software Requirements
- Python 3.11
- `Picamera2`
- `python-telegram-bot`
- `python-dotenv`
- `ultralytics`
- `cv2`

## Creating symlink
- Make sure to setup a sysmlink from the images directory to the local Nextjs website's public directory
    - this makes it so that the website is able to know where the images are
```bash
ln -s /home/raspberry/cat-food-security/images /home/raspberry/the-local-nextjs-website/public/images
```

