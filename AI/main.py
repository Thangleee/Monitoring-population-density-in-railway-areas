import time
import json
import cv2
import requests

from detector import PersonDetector
from tracker import PersonTracker
from roi import get_roi, draw_roi
from counter import PersonCounter
from visualizer import draw_track, draw_count
from ws_sever import run_ws_background, send_data
from csv_logger import CSVLogger
from warning import get_warning_level
from visualizer import draw_warning

# ======================
# CONFIG
# ======================
VIDEO_PATH = "video/vid2.mp4"
MODEL_PATH = "model/best.pt"
BACKEND_URL = "http://127.0.0.1:8000/data"
SEND_INTERVAL = 10   # gửi mỗi 10 frame

# ======================
# INIT
# ======================
logger = CSVLogger()
run_ws_background()

cap = cv2.VideoCapture(VIDEO_PATH)

detector = PersonDetector(MODEL_PATH)
tracker = PersonTracker()
counter = PersonCounter()
roi = get_roi()

frame_id = 0

# ======================
# MAIN LOOP
# ======================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # Detect
    detections = detector.detect(frame)

    # Track
    tracks = tracker.update(detections, frame)

    # update density
    counter.update(tracks, roi)
    density = counter.get_density()

    # Count
    for track in tracks:
        if not track.is_confirmed():
            continue

        l, t, r, b = map(int, track.to_ltrb())
        cx = int((l + r) / 2)
        cy = int((t + b) / 2)

        inside = cv2.pointPolygonTest(roi, (cx, cy), False) >= 0
        #counter.update(track.track_id, (cx, cy), roi)
        draw_track(frame, track, inside)

    # Draw UI
    draw_roi(frame, roi)
    count = counter.get_count()
    draw_count(frame, density)
    # CẢNH BÁO
    level, label, color = get_warning_level(count)
    draw_warning(frame, level, label, color)

    # SEND DATA (WS + CSV + BACKEND)
    if frame_id % SEND_INTERVAL == 0:
        payload = {
            "time": time.strftime("%H:%M:%S"),
            "count": count,
            "density": density,
            "warning_level": level,
            "warning_label": label
        }

        # WebSocket → Frontend realtime
        send_data(json.dumps(payload))

        # CSV log
        logger.log(density)

        # Backend FastAPI
        try:
            requests.post(BACKEND_URL, json=payload, timeout=0.2)
        except:
            print("⚠ Backend not available")

    # Show
    cv2.imshow("YOLO + DeepSORT", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
