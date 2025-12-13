
# Single Vs. Multithreading in computing

## **1 System Latency and Reaction Time Analysis**

To quantify the impact of the multithreaded architecture, a comparative analysis of the control loop frequency was conducted.

![Analysis of the control loop frequency ](../visualization/images/Figure_2.png)

- **Frequency Improvement:**

	The single-threaded architecture (Red) exhibited an average latency of 168.6 ms (~6 Hz), heavily bottlenecked by the blocking serial I/O calls required to read the LiDAR data.

	In contrast, the raw multithreaded performance initially achieved loop frequencies exceeding **8,000 Hz** (0.125 ms latency)—a roughly **1,360x increase** in raw processing speed.

However, processing data at 8 kHz provided diminishing returns for navigation while consuming excessive CPU resources and disk I/O for logging. Consequently, a **software throttle** was introduced to cap the frequency at **60 Hz (16.2 ms)**. This ensures the system remains highly responsive (Reaction Distance < 1.0 cm) while maintaining CPU efficiency for future sensor fusion tasks.

- **Safety Implications:**

	At the rover's cruising speed of $0.6 m/s$, this latency reduction translates directly to physical safety.

---

- **Old Architecture:** The vehicle traveled **10.1 cm** "blind" between sensor updates.
    
-   **New Architecture:** The vehicle travels only **1.0 cm** between updates.