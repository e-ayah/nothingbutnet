from ml.trend_analyzer import trends as analyze_trends
from ml.session_comparator import compare


ANGLE_NAMES = {
    "elbow_angle": "elbow angle",
    "knee_angle": "knee bend",
    "shoulder_angle": "shoulder angle",
}


def improvement_summary(sessions):
    if len(sessions) < 2:
        return "Analyze at least 2 shots to see your progress."

    trend_results = analyze_trends(sessions)
    comparisons = compare(sessions[0], sessions[-1])

    improved = []
    worsened = []

    for result in comparisons:
        checkpoint = result["checkpoint"]
        label = trend_results["labels"][checkpoint]

        # Use the trend analyzer when there are enough measurements.
        # Otherwise, fall back to comparing the first and last sessions.
        if label == "improving":
            direction = "better"
        elif label == "declining":
            direction = "worse"
        elif label == "flat":
            direction = "same"
        else:
            direction = result["direction"]

        if direction == "better":
            improved.append(ANGLE_NAMES[checkpoint])
        elif direction == "worse":
            worsened.append(ANGLE_NAMES[checkpoint])

    if not improved and not worsened:
        return "Your form is holding steady. Keep shooting!"

    messages = []

    if improved:
        messages.append(f"Your {' and '.join(improved)} improved")

    if worsened:
        messages.append(
            f"your {' and '.join(worsened)} moved farther from the ideal range"
        )

    return ". ".join(messages) + "."