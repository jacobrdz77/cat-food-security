from picamera2 import Picamera2
from ultralytics import YOLO
# import cv2

class YoloDetector():
    """
    YoloDetect - Uses Picamera2 & Yolo model to detect objects
    """
    # ID 15 for Cat
    def __init__(self, specific_model="yolov8n_ncnn_model", objects_to_detect=[15]):
        self.model = YOLO(specific_model, task="detect")
        self.objects_to_detect = objects_to_detect

    # image_frame has to come from Picamera2.capture_array()
    def detect(self, image_frame):
        print("Starting detection...")
        # Run YOLO model on the captured frame and store the results
        results = self.model(image_frame)
        detected_list = results[0].boxes.cls.tolist()

        for obj_id in self.objects_to_detect:
            if obj_id in detected_list:
                print("Cat detected!")
                return True
                # Send message to API with image attached
            if obj_id == 1:
                print("HUMAN detected!")
                return False
            elif not detected_list:
                print("Nothing detected...")
                return False
            else:
                print("Unknown detected!")
                return False
