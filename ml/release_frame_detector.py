# The elbow stays almost straight through the follow-through, so the single
# biggest angle usually lands late in the follow-through. Release is the first
# frame that gets within this many degrees of the biggest angle instead.
RELEASE_TOLERANCE = 10


def find_release_frame(frames, angles, side):
    '''
    frames: pose_extractor's result['frames']
    angles: elbow angle per frame, same order as frames (None if unknown),
            e.g. [a['elbow_angle'] for a in angles_for_video(frames)]
    side: 'left' or 'right' (shooting hand)
    returns (frame number, '') or (None, reason)
    '''
    wrist_idx, shoulder_idx = (16, 12) if side == 'right' else (15, 11)
    candidates = []  # (frame number, elbow angle) for frames with the wrist above the shoulder

    for i, frame in enumerate(frames):
        landmarks = frame['landmarks']
        if landmarks is None:
            continue

        angle = angles[i]
        if angle is None:
            continue

        wrist_y = landmarks[wrist_idx]['y']
        shoulder_y = landmarks[shoulder_idx]['y']
        if wrist_y is None or shoulder_y is None:
            # joint not seen in this frame
            continue
        if wrist_y >= shoulder_y:
            continue

        candidates.append((frame['frame'], angle))

    if not candidates:
        return (None, 'Wrist never goes above the shoulder')

    best_angle = max(angle for _, angle in candidates)
    for frame_number, angle in candidates:
        if angle >= best_angle - RELEASE_TOLERANCE:
            return (frame_number, '')
