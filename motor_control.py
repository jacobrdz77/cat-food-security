import gpiozero import Motor, PWMOutputDevice
import time
import signal

MOTOR_1 = 23 #GPIO 23
MOTOR_2= 24 #GPIO 24
PWM_PIN = 18 #GPIO 18 for PWM control

class DispenseMotor:
    """Used to rotate a auger screw to dispense food. """
    
    def __init__(self):
        self.motor = Motor(forward=MOTOR_1, backward=MOTOR_2, enable=PWM_PIN)

    def dispense_food(self):
        try:
            print("Running motor forward...")
            self.motor.forward(0.3)
            time.sleep(4)


            print("Running motor backwards...")
            self.motor.backward(0.3)
            time.sleep(1)

            print("Stopping motor...")
            self.motor.stop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        self.motor.stop()
        print("Motor stopped cleanly.")
        exit(0)

def main():
    try:
        motor = DispenseMotor()
        motor.dispense_food()

if __name__ == "__main__":
    main()
