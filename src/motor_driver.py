from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep
from src.constants import MAX_SPEED, MIN_SPEED, STALL_THRESHOLD, TURN_SPEED


class MotorDriver:
    def __init__(self):
        self.STBY = OutputDevice(26)

        # Left Motor (Group A)
        self.PWMA = PWMOutputDevice(17)
        self.AIN1 = OutputDevice(6)
        self.AIN2 = OutputDevice(5)

        # Right Motor (Group B)
        self.PWMB = PWMOutputDevice(27)
        self.BIN1 = OutputDevice(24)
        self.BIN2 = OutputDevice(23)

        self.STBY.on()  # Activate the motor driver immediately
        self.current_speed_val = 0.0  # Track actual speed (0.0 to 1.0)

    def _set_motor(self, pwm, in1, in2, speed):
        if speed > 0:
            # Forward
            in1.on()
            in2.off()
            pwm.value = speed
        elif speed < 0:
            # Backward
            in1.off()
            in2.on()
            pwm.value = abs(speed)
        else:
            # Stop
            in1.off()
            in2.off()
            pwm.value = 0

    def set_speed(self, target_speed):
        """
        Smoothly ramps the motor speed up or down.
        target_speed: Float between -1.0 (Full Back) and 1.0 (Full Forward)
        """
        target_speed = max(
            MIN_SPEED, min(target_speed, MAX_SPEED)
        )  # Make sure to respect -1.0 to 1.0 limits for motor safety

        # DEAD ZONE REMAPPING
        # If the code asks for speed 0.1, we physically send 0.2 (STALL_THRESHOLD).
        # If the code asks for speed 1.0, we physically send 1.0.
        current_abs = abs(target_speed)

        if current_abs < 0.05:
            # If asked for basically 0, just stop.
            final_pwm = 0.0
        else:
            # Formula: Scaled Output = Stall + (Target * (Max - Stall))
            # This compresses the 0.0-1.0 range into 0.25-1.0
            final_pwm = STALL_THRESHOLD + (current_abs * (MAX_SPEED - STALL_THRESHOLD))

            # Restore direction (negative speed)
            if target_speed < 0:
                final_pwm = -final_pwm

        step = 0.05  # Smaller step = smoother throttle ramp
        while abs(self.current_speed_val - final_pwm) > step:
            if self.current_speed_val < final_pwm:
                self.current_speed_val += step
            else:
                self.current_speed_val -= step
            # Apply the new intermediate speed to motors
            self._apply_speed(self.current_speed_val)

            # Small delay to make the ramp perceptible (e.g. 0.02s * 20 steps = 0.4s ramp)
            sleep(0.02)

        # Ensure we hit the exact target
        self.current_speed_val = final_pwm
        self._apply_speed(self.current_speed_val)

    def _apply_speed(self, speed):
        self._set_motor(self.PWMA, self.AIN1, self.AIN2, speed)
        self._set_motor(self.PWMB, self.BIN1, self.BIN2, speed)

    def move(self, speed):
        self.set_speed(speed)

    def turn_left(self):
        # "Tank Turn" (Left Back, Right Forward)
        self._set_motor(self.PWMA, self.AIN1, self.AIN2, -TURN_SPEED)
        self._set_motor(self.PWMB, self.BIN1, self.BIN2, TURN_SPEED)
        self.current_speed_val = 0  # Reset speed tracker since we broke flow

    def turn_right(self):
        self._set_motor(self.PWMA, self.AIN1, self.AIN2, TURN_SPEED)
        self._set_motor(self.PWMB, self.BIN1, self.BIN2, -TURN_SPEED)
        self.current_speed_val = 0

    def stop(self, force_stop=False):
        """
        force_stop=True:  Stops INSTANTLY (Emergency).
        force_stop=False: Stops smoothly (Normal).
        """
        if force_stop:
            self.current_speed_val = 0.0
            self._apply_speed(0.0)
        else:
            self.set_speed(0.0)

    def drive(self, left_speed, right_speed):
        """
        Manual differential drive control
        """
        left_speed = max(
            MIN_SPEED, min(left_speed, MAX_SPEED)
        )  # clamp to respect -1.0 <-> 1.0 speed for motor safety
        right_speed = max(MIN_SPEED, min(right_speed, MAX_SPEED))

        # if speed is too low to move, boost it to STALL_TRESHOLD to prevent stalling
        def remap(s):
            if abs(s) < 0.05:
                return 0.0  # stop if close to 0

            val = STALL_THRESHOLD + (abs(s) * (1 - STALL_THRESHOLD))
            return val if s > 0 else -val

        final_left = remap(left_speed)
        final_right = remap(right_speed)

        self._set_motor(self.PWMA, self.AIN1, self.AIN2, final_left)
        self._set_motor(self.PWMB, self.BIN1, self.BIN2, final_right)

    def cleanup(self):
        """
        Complete Shutdown: Stop motors and disable the driver chip.
        """
        self.set_speed(0.0)
        self.STBY.off()
        self.STBY.close()
        print("[MotorDriver] Driver disabled.")
