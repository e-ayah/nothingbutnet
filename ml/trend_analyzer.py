import numpy as np


RANGES = {
    "elbow_angle": (85, 100),
    "knee_angle": (150, 175),
    "shoulder_angle": (45, 75),
}

SLOPE_THRESHOLD = 0.5


def trends(sessions, ranges=RANGES):
    labels = {}
    trend_values = {}

    for angle_name, (lower, upper) in ranges.items():
        values = []

        for session in sessions:
            value = session["angles"].get(angle_name)

            if value is not None:
                values.append(value)

        if len(values) < 3:
            labels[angle_name] = "not enough data"
            trend_values[angle_name] = values
            continue

        distances = []

        for value in values:
            if value < lower:
                distance = lower - value
            elif value > upper:
                distance = value - upper
            else:
                distance = 0

            distances.append(distance)
        
        x = np.arange(len(distances))
        slope = np.polyfit(x, distances, 1)[0]

        if slope < -SLOPE_THRESHOLD:
            labels[angle_name] = "improving"
        elif slope > SLOPE_THRESHOLD:
            labels[angle_name] = "declining"
        else:
            labels[angle_name] = "flat"
        
        trend_values[angle_name] = values
        
    return {
        "labels": labels,
        "trends": trend_values,
    }