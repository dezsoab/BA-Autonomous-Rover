import argparse
import time
from src.motor_driver import MotorDriver
from src.lidar_only.lidar_strategy import LidarStrategy
from src.camera_only.camera_strategy import CameraStrategy
from src.fusion.fusion_strategy import FusionStrategy
from src.logger import ThesisLogger
from src.constants import *


def get_strategy(mode):
    if mode == "lidar":
        return LidarStrategy()
    # elif mode == 'camera': return CameraStrategy()
    # elif mode == 'fusion': return FusionStrategy()
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

    print(f"--- ROVER {ACTION_INIT}: {args.mode.upper()} ---")

    try:
        while True:
            is_safe, front_distance, left_distance, right_distance = brain.check_path()

            # calculate base speed (P-only controller)
            # slow down as rover gets closer to wall
            speed_factor = (front_distance - STOPPING_DIST_CM) / (
                SLOWDOWN_DIST_CM - STOPPING_DIST_CM
            )
            base_speed = max(
                MIN_APPROACH_SPEED, min(speed_factor * DEFAULT_SPEED, DEFAULT_SPEED)
            )

            # calculate steering
            turn_val = 0.0
            if left_distance < SIDE_CUSHION_DIST_CM:
                push = (SIDE_CUSHION_DIST_CM - left_distance) / SIDE_CUSHION_DIST_CM
                turn_val += push * TURN_SPEED

            if right_distance < SIDE_CUSHION_DIST_CM:
                push = (SIDE_CUSHION_DIST_CM - right_distance) / SIDE_CUSHION_DIST_CM
                turn_val -= push * TURN_SPEED

            if not is_safe:
                # emergency stop if too close
                print(f"CRITICAL OBSTACLE ({front_distance:.1f}cm) -> STOP")
                logger.log(
                    args.mode,
                    front_distance,
                    left_distance,
                    right_distance,
                    ACTION_BACKWARD,
                    f"L={left_motor_speed:.2f} R={right_motor_speed:.2f}",
                )
                rover.stop(force_stop=True)
                time.sleep(0.2)
                rover.drive(-0.3, -0.3)
                time.sleep(0.5)
                rover.stop()
                time.sleep(0.1)
                continue

            # Diferential drive
            left_motor_speed = base_speed + turn_val
            right_motor_speed = base_speed - turn_val

            rover.drive(left_motor_speed, right_motor_speed)

            logger.log(
                args.mode,
                front_distance,
                left_distance,
                right_distance,
                ACTION_DRIVE,
                f"L={left_motor_speed:.2f} R={right_motor_speed:.2f}",
            )
            time.sleep(
                0.016
            )  # <- 60 Hz Speed Limit => Time = cycle/target Hz => T=1/60

    except KeyboardInterrupt:
        print(f"{ACTION_STOP} received. Shutting down...")
    finally:
        print("Cleaning up resources...")
        rover.cleanup()
        brain.stop()


if __name__ == "__main__":
    main()
