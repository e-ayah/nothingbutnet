import csv
import matplotlib.pyplot as plt
import os

frames_no_smooth = []
y_no_smooth = []

frames_smooth = []
y_smooth = []

file_location = os.path.join(os.getcwd(), "nothingbutnet", "ml", "LandmarkProcessing")

# Load non-smoothed data
with open(os.path.join(file_location, "landmarksNoSmooth.csv"), "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["landmark"]) == 16:
            frames_no_smooth.append(int(row["frame"]))
            y_no_smooth.append(float(row["y"]))

# Load smoothed data
with open(os.path.join(file_location, "landmarksSmooth.csv"), "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["landmark"]) == 16:
            frames_smooth.append(int(row["frame"]))
            y_smooth.append(float(row["y"]))

# BOTH lines on the SAME graph
plt.plot(frames_no_smooth, y_no_smooth, label="No Smoothing")
plt.plot(frames_smooth, y_smooth, label="Smoothed")

plt.xlabel("Frame")
plt.ylabel("Right Wrist Y Position (pixels)")
plt.title("Right Wrist Y Position Over Time")

plt.legend()
plt.show()