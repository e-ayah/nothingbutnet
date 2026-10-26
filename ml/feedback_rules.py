from ml.tips import get_tip

NO_ANGLE_TIP = "We couldn't measure this angle. Film from the side with your whole body in view."

ANGLE_RANGES = {
    "elbow_angle": {
        "checkpoint": "elbow_alignment",
        "min": 85,
        "max": 100,
    },
    "knee_angle": {
        "checkpoint": "knee_bend",
        "min": 150,
        "max": 175,
    },
    "shoulder_angle": {
        "checkpoint": "shoulder_position",
        "min": 45,
        "max": 75,
    },
}

points_lost = 2

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

        tip = NO_ANGLE_TIP if angle is None else get_tip(rule["checkpoint"], angle, rule["min"], rule["max"])

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