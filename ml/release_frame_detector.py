# The elbow stays almost straight through the follow-through, so the single
# biggest angle usually lands late in the follow-through. Release is the first
# frame that gets within this many degrees of the biggest angle instead.
RELEASE_TOLERANCE = 10
MAX_GAP = 5
EXTENSION_ANGLE = 160
RULE = 'first_extension'

def fill_gaps(values, max_gap=MAX_GAP):
    """Fill runs of None up to max_gap long by drawing a straight line
    between the neighbors."""
    out = list(values)
    i = 0
    while i < len(out):
        if out[i] is None:
            j = i
            while j < len(out) and out[j] is None:
                j += 1
            if 0 < i and j < len(out) and (j - i) <= max_gap:
                a, b = out[i - 1], out[j]
                for k in range(i, j):
                    out[k] = a + (b - a) * (k - i + 1) / (j - i + 1)
            i = j
        else:
            i += 1
    return out

def _joint_y(frames, idx):
    '''Height (y) of one joint in every frame; None where it wasn't seen.'''
    ys = []
    for frame in frames:
        landmarks = frame['landmarks']
        ys.append(None if landmarks is None else landmarks[idx]['y'])
    return ys

def find_release_frame(frames, angles, side):
    '''
    frames: pose_extractor's result['frames']
    angles: elbow angle per frame, same order as frames (None if unknown),
            e.g. [a['elbow_angle'] for a in angles_for_video(frames)]
    side: 'left' or 'right' (shooting hand)
    returns (frame number, '') or (None, reason)
    '''
    wrist_idx, shoulder_idx = (16, 12) if side == 'right' else (15, 11)

    elbow = fill_gaps(angles)
    wrist_y = fill_gaps(_joint_y(frames, wrist_idx))
    shoulder_y = fill_gaps(_joint_y(frames, shoulder_idx))

    candidates = []
    for i, frame in enumerate(frames):
        if elbow[i] is None or wrist_y[i] is None or shoulder_y[i] is None:
            continue
        if wrist_y[i] >= shoulder_y[i]:
            continue
        candidates.append((frame['frame'], elbow[i], wrist_y[i]))

    if not candidates:
        return (None, 'Wrist never goes above the shoulder')

    if RULE == 'first_extension':
        for k in range(len(candidates) - 1):
            f1, a1, _ = candidates[k]
            f2, a2, _ = candidates[k + 1]
            if a1 >= EXTENSION_ANGLE and a2 >= EXTENSION_ANGLE and f2 == f1 + 1:
                return (f1, '')
        pass

    if RULE == 'wrist_peak':
        best = min(candidates, key=lambda c: c[2])
        return (best[0], '')

    best_angle = max(c[1] for c in candidates)
    for frame_number, angle, _ in candidates:
        if angle >= best_angle - RELEASE_TOLERANCE:
            return (frame_number, '')