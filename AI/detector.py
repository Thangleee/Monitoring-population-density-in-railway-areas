from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path, conf=0.15):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        results = self.model(
            frame,
            conf=self.conf,
            classes=[2],      # person
            imgsz=1280,
            verbose=False
        )

        detections = []

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        return detections
