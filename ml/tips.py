TIPS = {
    "elbow_alignment": {
        "good": "Great elbow alignment — keep your elbow under the ball.",
        "too_low": "Raise your elbow so it lines up under the ball.",
        "too_high": "Lower your elbow so it stays under the ball.",
    },
    "knee_bend": {
        "good": "Great knee bend — keep your legs ready to drive the shot.",
        "too_low": "Straighten your legs slightly before releasing the ball.",
        "too_high": "Bend your knees a little more before shooting.",
    },
    "shoulder_position": {
        "good": "Great shoulder position — keep it steady as you shoot.",
        "too_low": "Raise your shooting shoulder slightly as you prepare to shoot.",
        "too_high": "Lower your shooting shoulder slightly as you prepare to shoot.",
    },
}


def get_tip(checkpoint, angle, low, high):
    if angle < low:
        return TIPS[checkpoint]["too_low"]
    if angle > high:
        return TIPS[checkpoint]["too_high"]
    return TIPS[checkpoint]["good"]


if __name__ == "__main__":
    checkpoints = {
        "elbow_alignment": (85, 100),
        "knee_bend": (150, 175),
        "shoulder_position": (45, 75),
    }

    for checkpoint in checkpoints:
        low, high = checkpoints[checkpoint]
        print(checkpoint)
        print("Good:", get_tip(checkpoint, (low + high) / 2, low, high))
        print("Too low:", get_tip(checkpoint, low - 1, low, high))
        print("Too high:", get_tip(checkpoint, high + 1, low, high))
        print()
