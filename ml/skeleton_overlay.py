import cv2

def draw_skeleton(frame, landmarks, statuses, side):

    LEFT = {
        "shoulder": 11,
        "elbow": 13,
        "wrist": 15,
        "hip": 23,
        "knee": 25,
        "ankle": 27,
    }

    RIGHT = {
        "shoulder": 12,
        "elbow": 14,
        "wrist": 16,
        "hip": 24,
        "knee": 26,
        "ankle": 28,
    }

    GOOD = (0, 170, 0)
    NEEDS_WORK = (0, 120, 255)

    height, width = frame.shape[:2]
    radius = max(3, width // 200)
    thickness = max(1, width // 300)

    # Decide color from checkpoint status
    def get_color(checkpoint):
        if statuses.get(checkpoint) == "needs_work":
            return NEEDS_WORK
        return GOOD

    # Convert landmark to a usable point only if valid
    def get_point(landmark):
        if landmark is None:
            return None

        if landmark["visibility"] < 0.5:
            return None

        return (int(landmark["x"]), int(landmark["y"]))

    for body_side in [LEFT, RIGHT]:

        shoulder = get_point(landmarks[body_side["shoulder"]])
        elbow = get_point(landmarks[body_side["elbow"]])
        wrist = get_point(landmarks[body_side["wrist"]])
        hip = get_point(landmarks[body_side["hip"]])
        knee = get_point(landmarks[body_side["knee"]])
        ankle = get_point(landmarks[body_side["ankle"]])

        elbow_color = get_color("elbow_alignment")
        knee_color = get_color("knee_bend")
        shoulder_color = get_color("shoulder_position")

        # Draw lines only if both endpoints exist
        if shoulder is not None and elbow is not None:
            cv2.line(frame, shoulder, elbow, elbow_color, thickness)

        if elbow is not None and wrist is not None:
            cv2.line(frame, elbow, wrist, elbow_color, thickness)

        if shoulder is not None and hip is not None:
            cv2.line(frame, shoulder, hip, shoulder_color, thickness)

        if hip is not None and knee is not None:
            cv2.line(frame, hip, knee, knee_color, thickness)

        if knee is not None and ankle is not None:
            cv2.line(frame, knee, ankle, knee_color, thickness)

        # Draw circles only if that joint exists
        if shoulder is not None:
            cv2.circle(frame, shoulder, radius, shoulder_color, -1)

        if elbow is not None:
            cv2.circle(frame, elbow, radius, elbow_color, -1)

        if wrist is not None:
            cv2.circle(frame, wrist, radius, elbow_color, -1)

        if hip is not None:
            cv2.circle(frame, hip, radius, shoulder_color, -1)

        if knee is not None:
            cv2.circle(frame, knee, radius, knee_color, -1)

        if ankle is not None:
            cv2.circle(frame, ankle, radius, knee_color, -1)

    return frame