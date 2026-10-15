from ml.feedback_rules import ANGLE_RANGES

# same optimal ranges as the feedback, e.g. {"elbow_angle": (85, 100), ...}
RANGES = {name: (rule["min"], rule["max"]) for name, rule in ANGLE_RANGES.items()}

def distance_to_range(angle, low, high):
    if low <= angle and angle <= high:
        return 0
    elif angle <= low:
        return low - angle
    elif angle >= high:
        return angle - high

def compare(older, newer, ranges=RANGES):
    results = []
    
    for checkpoint, (low, high) in ranges.items():
        # processing/failed sessions have angles=None -> direction "unknown"
        before = (older.get("angles") or {}).get(checkpoint)
        after = (newer.get("angles") or {}).get(checkpoint)
        if before == None or after == None:
            delta = None
            direction = "unknown"
        else:
            delta = after - before
            change = distance_to_range(after, low, high) - distance_to_range(before,low,high)
            if abs(change) <= 1:
                direction = "same"
            elif change < 0:
                direction = "better"
            else:
                direction = "worse"
    
        results.append(
            {
                "checkpoint": checkpoint,
                "before": before,
                "after": after,
                "delta": delta,
                "direction": direction,
            }
        )
    return results