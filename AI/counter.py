import cv2
class PersonCounter:
    def __init__(self):
        self.current_ids = set()

    def update(self, tracks, roi):
        self.current_ids.clear()

        for track in tracks:
            if not track.is_confirmed():
                continue

            l, t, r, b = map(int, track.to_ltrb())
            cx = int((l + r) / 2)
            cy = int((t + b) / 2)

            if cv2.pointPolygonTest(roi, (cx, cy), False) >= 0:
                self.current_ids.add(track.track_id)

    def get_density(self):
        return len(self.current_ids)

    # SỐ NGƯỜI TỨC THỜI TRONG ROI
    def get_count(self):
        return len(self.current_ids)