import numpy as np
import mediapipe as mp

from mediapipe.python.solutions import pose as mp_pose

def calculate_angle(point_a, point_b, point_c):
    # Angle at point_b, given three points
    a, b, c = np.array(point_a), np.array(point_b), np.array(point_c)
    vector_ba = a - b
    vector_bc = c - b
    lengths = np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc)
    if lengths == 0:
        # two joints at the same spot -> no angle (avoids nan)
        return None
    cosine = np.dot(vector_ba, vector_bc) / lengths
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))
    return round(angle, 1)

def detect_shooting_side(frames):
    # returns shooting side given list of frames
    l_wrist, r_wrist = float('inf'), float('inf')
    L = mp_pose.PoseLandmark
    for item in frames:
        landmarks = item['landmarks']
        if landmarks is None:
            # no person found in this frame
            continue
        # left wrist is index 15, right wrist is index 16 (y is None if the joint wasn't seen)
        l_y = landmarks[L.LEFT_WRIST.value]['y']
        r_y = landmarks[L.RIGHT_WRIST.value]['y']
        if l_y is not None:
            l_wrist = min(l_wrist, l_y)
        if r_y is not None:
            r_wrist = min(r_wrist, r_y)
    if l_wrist < r_wrist:
        return 'left'
    else:
        return 'right'

def angles_for_frame(landmarks, side):
    L = mp_pose.PoseLandmark
    # returns elbow, knee, and shoulder angles given landmarks and side
    pt = lambda i: [landmarks[i.value]['x'], landmarks[i.value]['y']]
    if side == 'left':
        shoulder, elbow, wrist = L.LEFT_SHOULDER, L.LEFT_ELBOW, L.LEFT_WRIST
        hip, knee, ankle = L.LEFT_HIP, L.LEFT_KNEE, L.LEFT_ANKLE
    else:
        shoulder, elbow, wrist = L.RIGHT_SHOULDER, L.RIGHT_ELBOW, L.RIGHT_WRIST
        hip, knee, ankle = L.RIGHT_HIP, L.RIGHT_KNEE, L.RIGHT_ANKLE
    # check if angles are missing or reliable
    # check if visibility exists and is confident (>0.5) --> if so, then calculate angle, and if not, return None for that angle
    def is_reliable(joint):
        val = joint.value
        if val >= len(landmarks):
            return False
        vis = landmarks[val].get('visibility')
        if vis != None and vis > 0.5:
            return True
        else:
            return False
    # elbow angle
    if is_reliable(shoulder) and is_reliable(elbow) and is_reliable(wrist):
        elbow_angle = calculate_angle(pt(shoulder), pt(elbow), pt(wrist))
    else:
        elbow_angle = None
    # knee angle
    if is_reliable(hip) and is_reliable(knee) and is_reliable(ankle):
        knee_angle = calculate_angle(pt(hip), pt(knee), pt(ankle))
    else:
        knee_angle = None
    # shoulder angle
    if is_reliable(hip) and is_reliable(shoulder) and is_reliable(elbow):
        shoulder_angle = calculate_angle(pt(hip), pt(shoulder), pt(elbow))
    else:
        shoulder_angle = None
    return {
        'elbow_angle':    elbow_angle,
        'knee_angle':     knee_angle,
        'shoulder_angle': shoulder_angle,
    }

def angles_for_video(frames):
    # returns list of {'frame': n, 'elbow_angle': ..., ...}
    side = detect_shooting_side(frames) # left or right side
    result = []
    n = 0
    for item in frames:
        landmarks = item['landmarks']
        if landmarks is None:
            # no person found in this frame -> no angles
            angles = {'elbow_angle': None, 'knee_angle': None, 'shoulder_angle': None}
        else:
            angles = angles_for_frame(landmarks, side)
        # final result
        result += [{'frame': n, 'elbow_angle': angles['elbow_angle'], 'knee_angle': angles['knee_angle'], 'shoulder_angle': angles['shoulder_angle']}]
        n += 1
    return result