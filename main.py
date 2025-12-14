import argparse
import time
from src.motor_driver import MotorDriver
from src.lidar_only.lidar_strategy import LidarStrategy
from src.logger import ThesisLogger
from src.constants import *


def get_strategy(mode):
    if mode == "lidar":
        return LidarStrategy()
    else:
        raise ValueError("Invalid Mode")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", type=str, required=True, help="lidar, camera, fusion"
    )
    args = parser.parse_args()
    logger = ThesisLogger(args.mode)

    try:
        rover = MotorDriver()
        brain = get_strategy(args.mode)
    except Exception as e:
        print(f"Hardware Error: {e}")
        return

    print(f"--- ROVER {ACTION_INIT} ---")

    try:
        while True:
            front, left, right = brain.check_path()

            if front > SLOWDOWN_DIST_CM:
                base_speed = DEFAULT_SPEED
            else:
                base_speed = MIN_APPROACH_SPEED

            # GENTLE STEERING
            turn_val = 0.0

            if left < SIDE_CUSHION_DIST_CM:
                turn_val += (
                    SIDE_CUSHION_DIST_CM - left
                ) * STEER_SENSITIVITY  # Nudge Right

            if right < SIDE_CUSHION_DIST_CM:
                turn_val -= (
                    SIDE_CUSHION_DIST_CM - right
                ) * STEER_SENSITIVITY  # Nudge Left

            # Start steering away slightly before we hit the slowdown zone
            if front < SLOWDOWN_DIST_CM:
                if left < right:
                    turn_val += OBSTACLE_AVOIDANCE_BIAS
                else:
                    turn_val -= OBSTACLE_AVOIDANCE_BIAS

            # Max turn is 25% power difference
            turn_val = max(-0.25, min(turn_val, 0.25))

            # CRITICAL STOP & PRECISION TURN
            if front < CRITICAL_DIST_CM:
                print(f"CRITICAL ({front:.1f}cm) -> PRECISION TURN")
                rover.stop(force_stop=True)
                time.sleep(0.2)

                # Back up slowly
                escape_speed = STALL_THRESHOLD
                rover.drive(-escape_speed, -escape_speed)
                time.sleep(0.6)
                rover.stop()
                time.sleep(0.1)

                # Precision Pivot
                if left > right:
                    rover.drive(-escape_speed, escape_speed)  # Turn Left
                else:
                    rover.drive(escape_speed, -escape_speed)  # Turn Right

                time.sleep(0.5)
                rover.stop()
                time.sleep(0.2)
                continue

            # Drive
            left_motor = base_speed + turn_val
            right_motor = base_speed - turn_val

            rover.drive(left_motor, right_motor)

            logger.log(
                args.mode,
                front,
                left,
                right,
                ACTION_DRIVE,
                f"L={left_motor:.2f} R={right_motor:.2f}",
            )
            time.sleep(0.016)

    except KeyboardInterrupt:
        print(f"{ACTION_STOP} received.")
    finally:
        rover.cleanup()
        brain.stop()
        logger.close()


if __name__ == "__main__":
    main()
