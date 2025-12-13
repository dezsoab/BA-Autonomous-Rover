import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np


def plot_real_comparison():
    # 1. Find CSV files
    list_of_files = glob.glob("data_logs/*.csv")
    if len(list_of_files) < 2:
        print("Error: Need at least 2 log files.")
        return

    # Sort: Oldest (Index 0) vs Newest (Index -1)
    list_of_files.sort(key=os.path.getctime)
    oldest_file = list_of_files[0]
    newest_file = list_of_files[-1]

    print(f"Old: {os.path.basename(oldest_file)}")
    print(f"New: {os.path.basename(newest_file)}")

    # Helper: Extract Latencies
    def get_latencies(filename):
        try:
            df = pd.read_csv(
                filename, names=["Time", "Src", "F", "L", "R", "Act", "Det"], skiprows=1
            )
            # Combine dummy date to parse time
            df["Datetime"] = pd.to_datetime("2025-01-01 " + df["Time"], errors="coerce")
            lat = df["Datetime"].diff().dt.total_seconds() * 1000  # to ms
            return lat[(lat > 0) & (lat < 500)]  # Filter outliers
        except:
            return []

    old_data = get_latencies(oldest_file)
    new_data = get_latencies(newest_file)

    # Stats
    old_avg = old_data.mean()
    new_avg = new_data.mean()

    # --- PHYSICS CALCULATION ---
    ROBOT_SPEED_M_S = 0.6
    dist_old_cm = (old_avg / 1000.0) * ROBOT_SPEED_M_S * 100
    dist_new_cm = (new_avg / 1000.0) * ROBOT_SPEED_M_S * 100

    # --- PLOT ---
    fig, ax = plt.subplots(figsize=(12, 7))

    # Histograms with black edges to make them pop
    # We use 'density=True' to normalize heights if one file has way more lines than the other
    ax.hist(
        old_data,
        bins=50,
        range=(0, 250),
        color="salmon",
        alpha=0.6,
        edgecolor="black",
        label="Old (Single-Thread)",
    )
    ax.hist(
        new_data,
        bins=50,
        range=(0, 250),
        color="skyblue",
        alpha=0.8,
        edgecolor="black",
        label="New (Multi-Thread)",
    )

    # Vertical Mean Lines
    ax.axvline(old_avg, color="red", linestyle="--", linewidth=3)
    ax.axvline(new_avg, color="blue", linestyle="--", linewidth=3)

    # Annotations (The "Blind Distance" Metric)
    # Box for Old Robot
    text_old = (
        f"OLD ARCHITECTURE\n"
        f"Latency: {old_avg:.1f} ms\n"
        f"Reaction Dist: {dist_old_cm:.1f} cm\n"
        f"(Dangerous)"
    )
    ax.text(
        old_avg + 5,
        plt.ylim()[1] * 0.5,
        text_old,
        color="darkred",
        bbox=dict(facecolor="white", edgecolor="red", alpha=0.8),
    )

    # Box for New Robot
    text_new = (
        f"NEW ARCHITECTURE\n"
        f"Latency: {new_avg:.1f} ms\n"
        f"Reaction Dist: {dist_new_cm:.1f} cm\n"
        f"(Safe)"
    )
    ax.text(
        new_avg + 5,
        plt.ylim()[1] * 0.8,
        text_new,
        color="darkblue",
        bbox=dict(facecolor="white", edgecolor="blue", alpha=0.8),
    )

    ax.set_xlabel("Loop Latency (milliseconds)")
    ax.set_ylabel("Frequency (Normalized)")
    ax.set_title(
        f"Performance Analysis: From {dist_old_cm:.1f}cm to {dist_new_cm:.1f}cm Blind Distance"
    )
    ax.set_xlim(0, 250)  # Cut off empty space
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_real_comparison()
