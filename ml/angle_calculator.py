
import numpy as np
from mediapipe.python.solutions import pose as mp_pose


def calculate_angle(point_a, point_b, point_c):
    """Calculate the angle at point_b using three points."""
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)

    vector_ba = a - b
    vector_bc = c - b

    lengths = np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc)

    if lengths == 0:
        return None

    cosine = np.dot(vector_ba, vector_bc) / lengths
    cosine = np.clip(cosine, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine))

    return round(angle, 1)


def smooth(values, window=5):
    """Smooth angle measurements using a centered moving average."""
    radius = window // 2
    smoothed = []

    for i in range(len(values)):
        start = max(0, i - radius)
        end = min(len(values), i + radius + 1)

        nearby = [
            value for value in values[start:end]
            if value is not None
        ]

        if nearby:
            smoothed.append(round(float(np.mean(nearby)), 1))
        else:
            smoothed.append(None)

    return smoothed


def detect_shooting_side(frames):
    """Determine whether the player shoots with their left or right side."""
    l_wrist = float('inf')
    r_wrist = float('inf')

    L = mp_pose.PoseLandmark

    for item in frames:
        landmarks = item['landmarks']

        if landmarks is None:
            continue

        l_y = landmarks[L.LEFT_WRIST.value]['y']
        r_y = landmarks[L.RIGHT_WRIST.value]['y']

        if l_y is not None:
            l_wrist = min(l_wrist, l_y)

        if r_y is not None:
            r_wrist = min(r_wrist, r_y)

    if l_wrist < r_wrist:
        return 'left'

    return 'right'


def angles_for_frame(landmarks, side):
    """Calculate elbow, knee, and shoulder angles for one frame."""
    L = mp_pose.PoseLandmark

    if side == 'left':
        shoulder = L.LEFT_SHOULDER
        elbow = L.LEFT_ELBOW
        wrist = L.LEFT_WRIST

        hip = L.LEFT_HIP
        knee = L.LEFT_KNEE
        ankle = L.LEFT_ANKLE
    else:
        shoulder = L.RIGHT_SHOULDER
        elbow = L.RIGHT_ELBOW
        wrist = L.RIGHT_WRIST

        hip = L.RIGHT_HIP
        knee = L.RIGHT_KNEE
        ankle = L.RIGHT_ANKLE

    def is_reliable(joint):
        val = joint.value

        if val >= len(landmarks):
            return False

        point = landmarks[val]

        return (
            point.get('reliable', True)
            and point.get('visibility', 0) > 0.5
            and point.get('x') is not None
            and point.get('y') is not None
        )

    def pt(joint):
        point = landmarks[joint.value]
        return [point['x'], point['y']]

    # Elbow angle
    if (
        is_reliable(shoulder)
        and is_reliable(elbow)
        and is_reliable(wrist)
    ):
        elbow_angle = calculate_angle(
            pt(shoulder),
            pt(elbow),
            pt(wrist)
        )
    else:
        elbow_angle = None

    # Knee angle
    if (
        is_reliable(hip)
        and is_reliable(knee)
        and is_reliable(ankle)
    ):
        knee_angle = calculate_angle(
            pt(hip),
            pt(knee),
            pt(ankle)
        )
    else:
        knee_angle = None

    # Shoulder angle
    if (
        is_reliable(hip)
        and is_reliable(shoulder)
        and is_reliable(elbow)
    ):
        shoulder_angle = calculate_angle(
            pt(hip),
            pt(shoulder),
            pt(elbow)
        )
    else:
        shoulder_angle = None

    return {
        'elbow_angle': elbow_angle,
        'knee_angle': knee_angle,
        'shoulder_angle': shoulder_angle,
    }


def angles_for_video(frames):
    """Calculate angles for every frame in a video."""
    side = detect_shooting_side(frames)

    result = []

    for item in frames:
        landmarks = item['landmarks']

        if landmarks is None:
            angles = {
                'elbow_angle': None,
                'knee_angle': None,
                'shoulder_angle': None,
            }
        else:
            angles = angles_for_frame(landmarks, side)

        result.append({
            'frame': item['frame'],
            'elbow_angle': angles['elbow_angle'],
            'knee_angle': angles['knee_angle'],
            'shoulder_angle': angles['shoulder_angle'],
        })

    # Smooth elbow measurements to reduce noisy angle changes.
    elbow_angles = [
        item['elbow_angle'] for item in result
    ]

    smoothed_angles = smooth(elbow_angles, window=5)

    for i, angle in enumerate(smoothed_angles):
        result[i]['elbow_angle'] = angle

    return result
