import csv
import os
import time

class CSVLogger:
    def __init__(self, filepath="logs/people_count.csv"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath

        if not os.path.exists(filepath):
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["time", "count"])

    def log(self, count):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%H:%M:%S"),
                count
            ])
