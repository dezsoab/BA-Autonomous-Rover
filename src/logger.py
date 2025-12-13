import csv
import os
import time
import queue
import threading


class ThesisLogger:
    def __init__(self, mode):
        if not os.path.exists("data_logs"):
            os.makedirs("data_logs")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.filename = f"data_logs/rover_log_{mode}_{timestamp}.csv"

        self.log_queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._writer_loop, daemon=True)
        self.thread.start()

        print(f"[LOG] Logging to: {self.filename}")

    def log(self, source, front, left, right, action, notes=""):
        """
        Non-blocking log. Puts data in the queue and returns immediately.
        """
        timestamp = time.strftime("%H:%M:%S") + f".{int(time.time() * 1000) % 1000:03d}"

        row = [
            timestamp,
            source,
            f"{front:.1f}",
            f"{left:.1f}",
            f"{right:.1f}",
            action,
            notes,
        ]

        self.log_queue.put(row)

    def _writer_loop(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Timestamp",
                    "Mode",
                    "Front_Dist_cm",
                    "Left_Dist_cm",
                    "Right_Dist_cm",
                    "Action",
                    "Notes",
                ]
            )

            while self.running or not self.log_queue.empty():
                try:
                    row = self.log_queue.get(timeout=1.0)
                    writer.writerow(row)
                    file.flush()
                    self.log_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"[LOG ERROR]: {e}")

    def close(self):
        self.running = False
        self.thread.join()
        print(f"[LOG] Log file closed: {self.filename}")
