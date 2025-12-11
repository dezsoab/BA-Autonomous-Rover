# Hardware Control Layer
## lgpio

What it is: A low-level C library for controlling the General Purpose Input/Output (GPIO) pins on Linux.

Why we need it (Pi 5 Specific): The Raspberry Pi 5 uses a new custom I/O controller chip called the RP1. Older libraries (like RPi.GPIO) do not support this chip natively or reliably. lgpio is the bridge that allows Python to actually talk to the new hardware architecture of the Pi 5.

## gpiozero

What it is: A high-level electronics interface library.

Why we need it: It acts as a "wrapper" around lgpio. Instead of writing complex code to send specific electrical signals to pins, gpiozero allows us to use simple, readable classes like Motor, LED, or Robot. It simplifies the code significantly, making the "Motor Control" variable of the thesis easier to manage.

# Sensor Drivers

## LiDAR Interface (Direct Serial)

What it is: A direct Python script using `pyserial` and `struct`.
    
Why we need it: We interface directly with the InnoMaker LD19 via USB (`/dev/ttyUSB0`) at 230400 baud. We manually parse the 47-byte data packets to extract speed and angle data, avoiding overhead from third-party libraries that don't support this specific sensor.

## pyserial

What it is: A library that enables Python to communicate with the Serial (USB) ports.

Why we need it: This is a dependency for the LiDAR. The LiDAR connects via USB, which the Pi sees as a serial device (e.g., /dev/ttyUSB0).

# Perception & Computer Vision
## opencv-python (OpenCV)

What it is: The world's most popular open-source Computer Vision library.

Why we need it: It gives the robot "sight." We use it to capture frames from the camera, process them (grayscale, edge detection), and detect obstacles or lanes.

# Academic Data & Metrics
## pandas

What it is: A powerful data analysis and manipulation tool.

Why we need it: To make the thesis academic, we cannot just say "it drove well." We need quantitative data. We will use pandas to log performance metrics (e.g., Timestamp, Obstacle_Distance, Decision_Time, Success/Fail) into CSV files. These logs will generate the charts and graphs.

