#####################
## MOTOR CONSTANTS ##
MAX_SPEED = 1.0
MIN_SPEED = -1.0
DEFAULT_SPEED = 0.6
TURN_SPEED = 0.5
MIN_APPROACH_SPEED = 0.1  # Don't go slower than this until we stop
STALL_THRESHOLD = 0.2  # Below this speed, we consider the motor stalled due to heavy power bank and weight
## MOTOR CONSTANTS ##
#####################

#####################
## ACTION CONSTANTS ##
ACTION_FORWARD = "FORWARD"
ACTION_OBSTACLE = "OBSTACLE"
ACTION_TURN_LEFT = "TURN_LEFT"
ACTION_TURN_RIGHT = "TURN_RIGHT"
ACTION_AVOIDING = "AVOIDING"
ACTION_TURNED = "TURNED"
ACTION_STOP = "STOP"
ACTION_INIT = "INIT"
## ACTION CONSTANTS ##
#####################

#####################
## LIDAR CONSTANTS ##
# --- PROTOCOL CONSTANTS ---
BAUD_RATE = 230400
HEADER_BYTE_1 = b'\x54'
HEADER_BYTE_2 = b'\x2c'
PACKET_SIZE = 47
PAYLOAD_SIZE = 45 
POINTS_PER_PACKET = 12
ANGLE_DIVISOR = 100.0
MM_TO_CM = 10.0
LIDAR_OFFSET_DEG = 90
SCAN_DURATION_SEC = 0.15 

## LIDAR CONSTANTS ##
#####################

#####################
## DISTANCE CONSTANTS ##
MAX_VALID_DIST_CM = 200.0
STOPPING_DIST_CM = 20.0   
SLOWDOWN_DIST_CM = 90.0
CRITICAL_DIST_CM = 10.0
## DISTANCE CONSTANTS ##
#####################

#####################
## SECTOR CONSTANTS ##
SECTOR_BOUNDARIES = {
    'FRONT_START': 340, 'FRONT_END': 20,
    'LEFT_START': 270,  'LEFT_END': 340,
    'RIGHT_START': 20,  'RIGHT_END': 90 
}
## SECTOR CONSTANTS ##
#####################

#####################
## PORT CONSTANTS ##
DEFAULT_PORT = '/dev/ttyUSB0'
#####################
## PORT CONSTANTS ##