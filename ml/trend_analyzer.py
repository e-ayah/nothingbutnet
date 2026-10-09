import numpy as np

from ml.feedback_rules import ANGLE_RANGES


# same optimal ranges as the feedback, e.g. {"elbow_angle": (85, 100), ...}
RANGES = {name: (rule["min"], rule["max"]) for name, rule in ANGLE_RANGES.items()}

SLOPE_THRESHOLD = 0.5


# sessions: oldest first, each with an "angles" dict (None for processing/failed sessions)
def trends(sessions, ranges=RANGES):
    labels = {}
    trend_values = {}

    for angle_name, (lower, upper) in ranges.items():
        values = []

        for session in sessions:
            angles = session.get("angles") or {}  # skip sessions with no angles
            value = angles.get(angle_name)

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