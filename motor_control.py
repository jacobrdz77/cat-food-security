import gpiozero import Motor, PWMOutputDevice
import time

MOTOR_1 = 23 #GPIO 23
MOTOR_2= 24 #GPIO 24
PWM_PIN = 18 #GPIO 18 for PWM control

class DispenseMotor:
    """Used to rotate a auger screw to dispense food. """
    
    def __init__(self):
        self.motor = Motor(forward=MOTOR_1, backward=MOTOR_2, pwm=True)
        self.pwm_control = PWMOutputDevice(pin=PWM_PIN)

    def dispense_food(self):
        self.motor.forward(0.3)
        time.sleep(4)
        self.motor.backward(0.3)
        time.sleep(1)
        self.motor.stop()


def main():
    motor = DispenseMotor()
    motor.dispense_food()

if __name__ == "__main__":
    main()
