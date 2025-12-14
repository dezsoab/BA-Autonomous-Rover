import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.motor_driver import MotorDriver

# --- ADJUSTING THESE UNTIL IT DRIVES STRAIGHT ---
#  cheap motors not always give same rpm output...
LEFT_TRIM = 1
RIGHT_TRIM = 1
SPEED = 0.7
# ---------------------------------------------

try:
    rover = MotorDriver()
    print("Driving...")

    l_speed = SPEED * LEFT_TRIM
    r_speed = SPEED * RIGHT_TRIM

    rover.drive(l_speed, r_speed)
    time.sleep(5.0)
    rover.stop()
    print("Done.")

except Exception as e:
    print(e)
finally:
    rover.cleanup()
