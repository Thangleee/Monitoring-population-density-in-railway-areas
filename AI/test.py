import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

model = YOLO("model/best.pt")
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture("video/vid2.mp4")

roi = np.array([
    (300, 400),
    (980, 400),
    (1280, 720),
    (0, 720)
], np.int32)

counted_ids = set()
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.2, imgsz=640)
    detections = []

    if results[0].boxes is not None:
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            if cls == 2:  # person
                detections.append(([x1, y1, x2-x1, y2-y1], conf, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())
        cx = int((l + r)/ 2)
        cy = int((t + b) / 2)

        inside = cv2.pointPolygonTest(roi, (cx, cy), False) >= 0

        if inside:
            if track_id not in counted_ids:
                counted_ids.add(track_id)
                count += 1

            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        else:
            cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 1)

        cv2.putText(frame, f"ID:{track_id}", (l, t-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
        cv2.circle(frame, (cx,cy), 4, (255,0,0), -1)

    cv2.polylines(frame, [roi], True, (0,255,255), 2)
    cv2.putText(frame, f"Count: {count}", (30,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    cv2.imshow("YOLO + DeepSORT", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
