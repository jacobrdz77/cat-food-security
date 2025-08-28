from gpiozero import DistanceSensor
from time import sleep

TRIG_PIN = 23 
ECHO_PIN = 24 

def wait_for_in_range():
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, threshold_distance=0.2) # 20cm
    sensor.wait_for_in_range(timeout=None)
    print("ACTIVATED")


def main():
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
    # sensor.distance -> Returns in meters 
    while True:
        distance = sensor.distance * 100 # returns cm
        print(f"Distance: {distance}")
        sleep(1)


if __name__ == "__main__":
    main()
