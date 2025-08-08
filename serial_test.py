import serial
import time

ser = serial.Serial('/dev/serial0', 256000, timeout=1)
print("Serial port opened. Listening for data...")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).hex()
            print(f"Received: {data}")
        time.sleep(0.5)
except KeyboardInterrupt:
    ser.close()
    print("Closed.")
