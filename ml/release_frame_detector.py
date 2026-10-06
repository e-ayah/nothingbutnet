def find_release_frame(frames, angles, side):
    wrist_idx, shoulder_idx = (16, 12) if side == 'right' else (15, 11)
    best_frame = None
    best_angle = None

    for i, frame in enumerate(frames):
        landmarks = frame['landmarks']
        if landmarks is None:
            continue

        angle = angles[i]
        if angle is None:
            continue

        wrist_y = landmarks[wrist_idx]['y']
        shoulder_y = landmarks[shoulder_idx]['y']
        if wrist_y >= shoulder_y:
            continue

        if best_angle is None or angle > best_angle:
            best_angle = angle
            best_frame = frame['frame']

    if best_frame is None:
        return (None, 'Wrist never goes above the shoulder')

    return (best_frame, '')