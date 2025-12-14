#####################
## MOTOR CONSTANTS ##
DEFAULT_SPEED = 0.55
MIN_APPROACH_SPEED = 0.25
STALL_THRESHOLD = 0.25
#####################

#####################
## TUNING CONSTANTS ##
STEER_SENSITIVITY = 0.005  # Low value = Gentle curves. High value = Twitchy steering.

OBSTACLE_AVOIDANCE_BIAS = (
    0.10  # Fixed steering offset applied when an object is detected ahead
)
#####################

#####################
## ACTION CONSTANTS ##
ACTION_DRIVE = "DRIVE"
ACTION_STOP = "STOP"
ACTION_INIT = "INIT"
#####################

#####################
## DISTANCE CONSTANTS ##
MAX_VALID_DIST_CM = 250.0
SLOWDOWN_DIST_CM = 55.0  # Below this, we slow to MIN_APPROACH_SPEED
CRITICAL_DIST_CM = 15.0  # Below this, we stop and escape
SIDE_CUSHION_DIST_CM = 35.0  # If wall is further than this, drive straight
#####################

#####################
## LIDAR CONSTANTS ##
BAUD_RATE = 230400
HEADER_BYTE_1 = b"\x54"
HEADER_BYTE_2 = b"\x2c"
PACKET_SIZE = 47
PAYLOAD_SIZE = 45
POINTS_PER_PACKET = 12
ANGLE_DIVISOR = 100.0
MM_TO_CM = 10.0
LIDAR_OFFSET_DEG = 90
#####################

#####################
## SECTOR CONSTANTS ##
SECTOR_BOUNDARIES = {
    "FRONT_START": 340,
    "FRONT_END": 20,
    "LEFT_START": 270,
    "LEFT_END": 340,
    "RIGHT_START": 20,
    "RIGHT_END": 90,
}
#####################

#####################
## PORT CONSTANTS ##
DEFAULT_PORT = "/dev/ttyUSB0"
#####################
