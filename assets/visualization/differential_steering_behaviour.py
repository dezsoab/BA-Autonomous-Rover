import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


def plot_log():
    # 1. Find the newest CSV file in data_logs/
    list_of_files = glob.glob("data_logs/*.csv")
    if not list_of_files:
        print("Error: No CSV files found in 'data_logs/' folder.")
        print("Current working directory:", os.getcwd())
        return

    latest_log = max(list_of_files, key=os.path.getctime)
    print(f"Plotting Real Data from: {latest_log}")

    # 2. Load Data (Skip header row)
    headers = ["Time", "Source", "Front", "Left", "Right", "Action", "Details"]
    try:
        df = pd.read_csv(latest_log, names=headers, skiprows=1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 3. Clean Data (Parse "L=0.60 R=0.50" strings)
    def extract_speeds(row):
        details = str(row["Details"])
        l, r = 0.0, 0.0
        if "L=" in details:
            parts = details.split(" ")
            for p in parts:
                if p.startswith("L="):
                    l = float(p.split("=")[1])
                if p.startswith("R="):
                    r = float(p.split("=")[1])
        return pd.Series([l, r])

    df[["SpeedL", "SpeedR"]] = df.apply(extract_speeds, axis=1)

    # Convert text to numbers, force errors to NaN
    for col in ["Front", "Left", "Right"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Slice the data to see the "middle" of the run (e.g.:20k lines are too cluttered)
    df = df.iloc[1000:3000]

    # 4. Plot
    plt.figure(figsize=(14, 10))

    # Subplot 1: Sensor Data
    plt.subplot(2, 1, 1)
    plt.plot(df["Front"], label="Front", color="blue", linewidth=1)
    plt.plot(df["Left"], label="Left", color="green", alpha=0.6)
    plt.plot(df["Right"], label="Right", color="red", alpha=0.6)
    plt.axhline(y=25, color="black", linestyle="--", label="Stop Threshold")
    plt.ylim(0, 250)  # Cut off the 999 initialization spikes
    plt.title("Lidar Sensor Input (Environment)")
    plt.ylabel("Distance (cm)")
    plt.legend()
    plt.grid(True)

    # Subplot 2: Motor Response
    plt.subplot(2, 1, 2)
    plt.plot(df["SpeedL"], label="Left Motor", color="green")
    plt.plot(df["SpeedR"], label="Right Motor", color="red")
    plt.ylim(-1.0, 1.0)
    plt.title("Differential Steering Output (Reaction)")
    plt.ylabel("Motor Speed")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_log()
