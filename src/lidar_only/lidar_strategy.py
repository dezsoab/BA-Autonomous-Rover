# --- LIDAR IMPLEMENTATION ---
import threading
from src.interfaces import ObstacleStrategy
import serial
import struct

from src.constants import (
    BAUD_RATE,
    HEADER_BYTE_1,
    HEADER_BYTE_2,
    PACKET_SIZE,
    PAYLOAD_SIZE,
    POINTS_PER_PACKET,
    ANGLE_DIVISOR,
    MM_TO_CM,
    LIDAR_OFFSET_DEG,
    MAX_VALID_DIST_CM,
    STOPPING_DIST_CM,
    SECTOR_BOUNDARIES,
    DEFAULT_PORT,
)


class LidarStrategy(ObstacleStrategy):
    def __init__(self, port=None):
        if port is None:
            port = DEFAULT_PORT

        self.ser = serial.Serial(port, BAUD_RATE, timeout=1)
        self.front_dist = 999.0
        self.left_dist = 999.0
        self.right_dist = 999.0

        self.running = False
        self.thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.start()

    def start(self):
        self.running = True
        self.thread.start()
        print("[LidarStrategy] Background thread started.")

    def _get_sector(self, angle):
        """Returns 'FRONT', 'LEFT', 'RIGHT', or None"""
        if (
            angle >= SECTOR_BOUNDARIES["FRONT_START"]
            or angle < SECTOR_BOUNDARIES["FRONT_END"]
        ):
            return "FRONT"
        elif SECTOR_BOUNDARIES["LEFT_START"] <= angle < SECTOR_BOUNDARIES["LEFT_END"]:
            return "LEFT"
        elif SECTOR_BOUNDARIES["RIGHT_START"] <= angle < SECTOR_BOUNDARIES["RIGHT_END"]:
            return "RIGHT"
        return None

    def _scan_loop(self):
        """
        THE BACKGROUND WORKER.
        This runs forever in a separate thread.
        It constantly updates self.front_dist, self.left_dist, etc.
        """
        # 1. Flush Buffer
        self.ser.reset_input_buffer()

        while self.running:
            if self.ser.in_waiting > PACKET_SIZE:
                if (
                    self.ser.read() == HEADER_BYTE_1
                    and self.ser.read() == HEADER_BYTE_2
                ):
                    data = self.ser.read(PAYLOAD_SIZE)
                    if len(data) != PAYLOAD_SIZE:
                        continue

                    # Decode Angles
                    start_angle = struct.unpack("<H", data[2:4])[0] / ANGLE_DIVISOR
                    end_angle = struct.unpack("<H", data[40:42])[0] / ANGLE_DIVISOR
                    if end_angle < start_angle:
                        end_angle += 360
                    step = (end_angle - start_angle) / (POINTS_PER_PACKET - 1)

                    # Process Points
                    for i in range(POINTS_PER_PACKET):
                        raw_dist_pos = 4 + (i * 3)
                        dist_mm = struct.unpack(
                            "<H", data[raw_dist_pos : raw_dist_pos + 2]
                        )[0]
                        dist_cm = dist_mm / MM_TO_CM

                        raw_angle = start_angle + (i * step)
                        corrected_angle = (raw_angle + LIDAR_OFFSET_DEG) % 360

                        sector = self._get_sector(corrected_angle)

                        if 0 < dist_cm < MAX_VALID_DIST_CM:
                            if sector == "FRONT":
                                if dist_cm < self.front_dist:
                                    self.front_dist = dist_cm
                                else:
                                    self.front_dist += 1  # if I don't see the obstacle anymore, it might be gone and stop halucinating?
                            elif sector == "LEFT":
                                if dist_cm < self.left_dist:
                                    self.left_dist = dist_cm
                                else:
                                    self.left_dist += 1
                            elif sector == "RIGHT":
                                if dist_cm < self.right_dist:
                                    self.right_dist = dist_cm
                                else:
                                    self.right_dist += 1

    def check_path(self):
        return self.front_dist, self.left_dist, self.right_dist

    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)
        self.ser.close()
        print("[LidarStrategy] Thread stopped and port closed.")
