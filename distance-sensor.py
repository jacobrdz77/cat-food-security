from gpiozero import DistanceSensor
from time import sleep

TRIG_PIN = 23 
ECHO_PIN = 24 


def main():
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

    while True:
        distance = sensor.distance * 100 # returns cm
        print(f"Distance: {distance}")
        sleep(1)


if __name__ == "__main__":
    main()
