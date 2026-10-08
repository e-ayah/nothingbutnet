# Boundaries are inclusive
# 

ANGLE_RANGES = {
    "elbow_angle": {
        "checkpoint": "elbow_alignment",
        "min": 85,
        "max": 100,
        "good_tip": "Great elbow position. Keeping it under the ball from 85-100 degrees gives you a consistent release.",
        "needs_work_tip": "Your elbow is drifting out of the ideal range. Make sure to keep it between 85-100 degrees and under the ball for a consistent release.",
    },
    "knee_angle": {
            "checkpoint": "knee_bend",
            "min": 150,
            "max": 175,
            "good_tip": "Good knee bend. Keeping your knee bent between 150-175 degrees gives you a good drive into your shot.",
            "needs_work_tip": "Your knees are hurting your shot. Make sure to keep the bend between 150-175 degrees so that your legs can work with your shot and not against it.",
    },
    "shoulder_angle": {
            "checkpoint": "shoulder_position",
            "min": 45,
            "max": 75,
            "good_tip": "Nice shoulder angle. Keeping it between 45-75 degrees gives you great control over your shot trajectory.",
            "needs_work_tip": "Careful of your shoulder. Keeping it between 45-75 degrees gives you the needed control over your shot trajectory.",
    }
}

points_lost = 2

# Scoring Rules:
# Start at 100 and for each angle outside its range subtract points_lost 
# points for every degree it is outside. Angles inside the range on the 
# boundaries do not lose and points and the final score is kept 
# between 0 and 100 and returned as an int.
def evaluate_form(angles:dict) -> dict:
    feedback = []
    score = 100

    for key, rule in ANGLE_RANGES.items():
        angle = angles[key]

        if angle < rule["min"]:
            degrees_off = rule["min"] - angle
        elif angle > rule["max"]:
            degrees_off = angle - rule["max"]
        else:
            degrees_off = 0

        if degrees_off == 0:
            status = "good"
            tip = rule["good_tip"]
        else:
            status = "needs_work"
            tip = rule["needs_work_tip"]
            score -= degrees_off * points_lost


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
