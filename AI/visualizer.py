import cv2

def draw_track(frame, track, inside):
    l, t, r, b = map(int, track.to_ltrb())
    color = (0, 255, 0) if inside else (0, 0, 255)

    cv2.rectangle(frame, (l, t), (r, b), color, 2)
    cv2.putText(frame, f"ID:{track.track_id}",
                (l, t - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                color, 2)

def draw_count(frame, count):
    cv2.putText(frame, f"Count: {count}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (0, 0, 255), 3)

def draw_warning(frame, level, text, color):
    cv2.putText(
        frame,
        f"ALERT: {text}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        3
    )
