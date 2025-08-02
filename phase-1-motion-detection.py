from gpiozero import MotionSensor
import time

def on_motion(e):
    print(f"MOOVING: is Active? {e.is_active}")
    
def on_no_motion(e):
    print(f"Is Active: {e.is_active}")

# GPIO 4 (PIN 7)
pir = MotionSensor(4)
pir.when_no_motion = on_no_motion
pir.when_motion = on_motion


try:
    while True:
        # print("Waiting.")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    

