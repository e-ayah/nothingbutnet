# The elbow stays almost straight through the follow-through, so the single
# biggest angle usually lands late in the follow-through. Release is the first
# frame that gets within this many degrees of the biggest angle instead.
RELEASE_TOLERANCE = 10



# The elbow stays almost straight through the follow-through.
RELEASE_TOLERANCE = 10


def find_release_frame(frames, angles, side):
    '''
    frames: pose_extractor's result['frames']
    angles: elbow angle per frame
    side: 'left' or 'right'
    returns (frame number, '') or (None, reason)
    '''

    wrist_idx, shoulder_idx = (16, 12) if side == 'right' else (15, 11)

    candidates = []

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
            continue

        if wrist_y >= shoulder_y:
            continue

        candidates.append((frame['frame'], angle))

    if not candidates:
        return (None, 'Wrist never goes above the shoulder')

    # DEBUG: Print elbow angles around the actual release
    print("\n========== ELBOW ANGLE DEBUG ==========")

    for i, frame in enumerate(frames):
        frame_number = frame['frame']

        if 50 <= frame_number <= 125:
            landmarks = frame['landmarks']

            if landmarks is None:
                print(f"Frame {frame_number}: NO LANDMARKS")
                continue

            print(
                f"Frame: {frame_number:3} | "
                f"Elbow: {angles[i]} | "
                f"Landmarks: {len(landmarks)}"
            )

    # Existing release detection logic
    best_angle = max(angle for _, angle in candidates)
    threshold = best_angle - RELEASE_TOLERANCE

    print("\nBest elbow angle:", best_angle)
    print("Release threshold:", threshold)

    for frame_number, angle in candidates:
        if angle >= threshold:
            print("DETECTED RELEASE FRAME:", frame_number)
            print("======================================\n")
            return (frame_number, '')

    return (None, 'Could not determine release frame')
