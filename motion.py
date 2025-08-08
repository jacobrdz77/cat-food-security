from LD2410 import *
import time
import logging

def radar_sensor():
    print("Starting LD2410...")
    radar = LD2410(port="/dev/serial0", verbosity=logging.DEBUG)

    print(f"Radar: {radar}")

    # detection_params = radar.read_detection_params()
    # print(detection_params)

    radar.enable_engineering_mode()
    radar.start()
    mac_address = radar.bt_query_mac()
    print(f"MAC addres: {mac_address}")

    print("Started!")

    try:
        for _ in range(10):
            print(radar.get_data())
            time.sleep(1)
    except Exception as e:
        print(f"Error reading LD2410 sensor data: {e}")
    finally:
        radar.stop()


if __name__ == "__main__":
    radar_sensor()

