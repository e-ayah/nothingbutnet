from ml.tips import get_tip

# Sixers#02: 10th–90th percentile of angles at hand-marked release frames
# on 20 made shots (n = 14 elbow, 15 knee, 16 shoulder), rounded to 5°.
ANGLE_RANGES = {
    "elbow_angle": {
        "checkpoint": "elbow_alignment",
        "min": 115,
        "max": 165,
    },
    "knee_angle": {
        "checkpoint": "knee_bend",
        "min": 140,
        "max": 170,
    },
    "shoulder_angle": {
        "checkpoint": "shoulder_position",
        "min": 10,
        "max": 150,
    },
}

points_lost = 2

# Scoring Rules:
# Start at 100 and for each angle outside its range subtract points_lost
# points for every degree it is outside. Angles inside the range or on the
# boundaries lose no points, and the final score is kept between 0 and 100
# and returned as an int.
# Angles that are missing or None (joint not visible) are skipped: no
# feedback item and no points lost.
def evaluate_form(angles: dict) -> dict:
    feedback = []
    score = 100

    for key, rule in ANGLE_RANGES.items():
        angle = angles.get(key)
        if angle is None:
            continue

        if angle < rule["min"]:
            degrees_off = rule["min"] - angle
        elif angle > rule["max"]:
            degrees_off = angle - rule["max"]
        else:
            degrees_off = 0

        if degrees_off == 0:
            status = "good"
        else:
            status = "needs_work"
            score -= degrees_off * points_lost

        tip = get_tip(rule["checkpoint"], angle, rule["min"], rule["max"])

        feedback.append(
            {
                "checkpoint": rule["checkpoint"],
                "angle": angle,
                "status": status,
                "tip": tip,
            }
        )

    score = int(round(max(0, min(100, score))))
    return {"feedback": feedback, "overall_score": score}