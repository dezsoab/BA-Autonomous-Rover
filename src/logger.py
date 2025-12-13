import csv
import os
from datetime import datetime


class ThesisLogger:
    def __init__(self, mode):
        # 1. Get the folder where THIS script (logger.py) lives
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Go up one level to find the Project Root (BA-Autonomous-Rover)
        project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

        # 3. Define the logs folder path safely
        self.log_folder = os.path.join(project_root, "data_logs")

        # 4. Create the folder if it doesn't exist (safety check)
        os.makedirs(self.log_folder, exist_ok=True)

        # 5. Create filename
        filename = f"rover_log_{mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.filepath = os.path.join(self.log_folder, filename)

        # Open file and write header
        with open(self.filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
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

        print(f"[LOG] Logging to: {self.filepath}")

    def log(self, mode, front, left, right, action, notes=""):
        try:
            with open(self.filepath, mode="a", newline="") as f:
                writer = csv.writer(f)
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                writer.writerow(
                    [
                        timestamp,
                        mode,
                        f"{front:.1f}",
                        f"{left:.1f}",
                        f"{right:.1f}",
                        action,
                        notes,
                    ]
                )
        except Exception as e:
            print(f"Logging Error: {e}")
