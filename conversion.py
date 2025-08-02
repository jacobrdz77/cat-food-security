from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# Formats the yolov8n.pt Nano model to format NCNN for faster FPS
model.export(format="ncnn", imgsz=640)
