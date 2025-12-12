import argparse
import time
from src.motor_driver import MotorDriver
from src.lidar_only.lidar_strategy import LidarStrategy
from src.camera_only.camera_strategy import CameraStrategy
from src.fusion.fusion_strategy import FusionStrategy
from src.logger import ThesisLogger
from src.constants import *

def get_strategy(mode):
    if mode == 'lidar': return LidarStrategy()
    # elif mode == 'camera': return CameraStrategy()
    # elif mode == 'fusion': return FusionStrategy()
    else: raise ValueError("Invalid Mode")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True, help='lidar, camera, fusion')
    args = parser.parse_args()
    logger = ThesisLogger(args.mode)

    try:
        rover = MotorDriver()
        brain = get_strategy(args.mode)
    except Exception as e:
        print(f"Hardware Error: {e}")
        return

    print(f"--- ROVER STARTED: {args.mode.upper()} ---")

    try:
        while True:
            is_safe, front_distance, left_distance, right_distance = brain.check_path()

            if is_safe:
                target_speed = DEFAULT_SPEED
                
                if front_distance < SLOWDOWN_DIST_CM:
                    # 1. Calculate the proportion (0.0 to 1.0)
                    # (Current - Stop) / (StartSlow - Stop)
                    # Example: At 70cm -> (70-40)/(100-40) = 30/60 = 0.5 (Half speed)
                    proportion = (front_distance - STOPPING_DIST_CM)/(SLOWDOWN_DIST_CM - STOPPING_DIST_CM)

                    # 2. Scale speed
                    target_speed = proportion * DEFAULT_SPEED
                    
                    # 3. Clamp: Don't go so slow the motor stalls (e.g., keep at least MIN_APPROACH_SPEED)
                    target_speed = max(target_speed, MIN_APPROACH_SPEED)

                print(f"{ACTION_FORWARD} Clear ({front_distance:.1f}cm) -> Speed: {target_speed:.2f}")
                logger.log(args.mode, front_distance, left_distance, right_distance, ACTION_FORWARD, f"Speed={target_speed:.2f}")
                
                rover.move(target_speed)
            else:
                rover.stop(front_distance < CRITICAL_DIST_CM)      
                print(f"[{args.mode.upper()}] OBSTACLE ({front_distance:.1f} cm) -> {ACTION_AVOIDING}")
                logger.log(mode=args.mode, front=front_distance,left=left_distance,right=right_distance, action=ACTION_AVOIDING, notes="Obstacle Detected")
                
                if left_distance > right_distance:
                    print(f"   -> {ACTION_TURN_LEFT} (L:{left_distance:.1f} > R:{right_distance:.1f})")
                    rover.turn_left()
                else:
                    print(f"   -> {ACTION_TURN_RIGHT} (R:{right_distance:.1f} > L:{left_distance:.1f})")
                    rover.turn_right()
                
                time.sleep(0.2) 
                rover.stop()
                time.sleep(0.2)
                logger.log(mode=args.mode, front=front_distance,left=left_distance,right=right_distance, action=ACTION_TURNED, notes="Avoidance Maneuver Completed")
            
    except KeyboardInterrupt:
        print(f"{ACTION_STOP} received. Shutting down...")
    finally:
        print("Cleaning up resources...")
        rover.cleanup()
        brain.stop()

if __name__ == "__main__":
    main()