import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose


def draw_angle_labels(frame, landmarks, angles, side):
    """
    Draw elbow, knee, and shoulder angle labels on the frame.

    Parameters:
        frame: OpenCV image
        landmarks: pose landmarks
        angles: dictionary like:
            {
                'elbow_angle': 92.3,
                'knee_angle': 165.1,
                'shoulder_angle': 58.7
            }
        side: 'left' or 'right'

    Returns:
        frame with angle labels drawn on it
    """

    height, width = frame.shape[:2]

    # Make font size depend on image width

    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = min(3, width // 200)
    font_scale = min(3, width // 200)

    L = mp_pose.PoseLandmark

    # Pick landmarks depending on which side we're displaying
    if side.lower() == 'right':
        joint_landmarks = {
            'elbow_angle': L.RIGHT_ELBOW,
            'knee_angle': L.RIGHT_KNEE,
            'shoulder_angle': L.RIGHT_SHOULDER
        }

    elif side.lower() == 'left':
        joint_landmarks = {
            'elbow_angle': L.LEFT_ELBOW,
            'knee_angle': L.LEFT_KNEE,
            'shoulder_angle': L.LEFT_SHOULDER
        }

    else:
        raise ValueError("side must be 'left' or 'right'")

    for angle_name, landmark_type in joint_landmarks.items():
        angle = angles.get(angle_name)

        # Angle may be None
        if angle is None:
            continue

        landmark = landmarks[landmark_type.value]

        x = int(landmark['x'])
        y = int(landmark['y'])

        # Move text slightly away from the joint
        position = (x + 10, y - 10)

        text = f"{round(angle)} deg"

        # text_width returns how many pixels wide rendered text, text_height is how tall pixels is, baseline is extra pixels below text baseline
        (text_width, text_height), baseline = cv2.getTextSize(
            text,
            font,
            font_scale,
            thickness
        )

        padding_x = 8
        padding_y = 6

        # calculating entire box width
        box_width = text_width + 2 * padding_x
        box_height = text_height + baseline + 2 * padding_y

        # Upper left hand corner of label box
        box_x1 = x + 10
        box_y1 = y - 10 - box_height

        # Keep box inside frame
        box_x1 = max(0, min(box_x1, width - box_width)) # highest
        box_y1 = max(0, min(box_y1, height - box_height)) # lowest

        box_x2 = box_x1 + box_width
        box_y2 = box_y1 + box_height

        cv2.rectangle(
            frame,
            (box_x1, box_y1),
            (box_x2, box_y2),
            (40, 40, 40),
            -1
        )

        # Center text horizontally
        text_x = box_x1 + (box_width - text_width) // 2

        # Center text vertically
        text_y = box_y1 + (box_height + text_height - baseline) // 2 + 3

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (box_x1, box_y1),
            (box_x2, box_y2),
            (100, 100, 100),
            -1
        )

        alpha = 0.3

        cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0,
            frame
        )

        # Draw text AFTER blending
        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )

    return frame