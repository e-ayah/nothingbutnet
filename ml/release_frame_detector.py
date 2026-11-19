# The elbow stays almost straight through the follow-through, so the single
# biggest angle usually lands late in the follow-through. Release is the first
# frame that gets within this many degrees of the biggest angle instead.
RELEASE_TOLERANCE = 10
MAX_GAP = 5
EXTENSION_ANGLE = 160
RULE = 'first_extension'

# Finals#04: refuse to guess on footage we can't trust.
MAX_GAP_NEAR_RELEASE = 5   # frames with no pose allowed within ±RELEASE_WINDOW of the release
RELEASE_WINDOW = 8
SPLICE_JUMP = 2.5          # body center moves more than this many torso lengths per frame (and stays)
SPLICE_SIZE_RATIO = 1.8    # torso suddenly this much bigger/smaller
MAX_TORSO_TILT = 45        # median shoulder->hip angle from vertical; more = sideways video

REASON_POSE_LOST = 'Pose lost near the release - film from the side with your whole body in view'
REASON_ROTATED = 'The video looks sideways - film in portrait or landscape without rotating the phone mid-recording'
REASON_SPLICED = ('The tracked person jumps or changes mid-clip (a cut, or someone else in frame) - '
                  'film one continuous take with only the shooter in view')

L_SHOULDER, R_SHOULDER, L_HIP, R_HIP = 11, 12, 23, 24


def missing_near(frames, candidate, window=RELEASE_WINDOW):
    """Longest run of frames with no landmarks within ±window of the candidate frame."""
    index = {f['frame']: i for i, f in enumerate(frames)}
    i = index.get(candidate)
    if i is None:
        return 0
    longest = run = 0
    for f in frames[max(0, i - window): i + window + 1]:
        run = run + 1 if f['landmarks'] is None else 0
        longest = max(longest, run)
    return longest


def _torso(landmarks):
    '''(center x, center y, torso length) from shoulders + hips, or None if any is unseen.'''
    pts = [landmarks[i] for i in (L_SHOULDER, R_SHOULDER, L_HIP, R_HIP)]
    if any(p['x'] is None or p['y'] is None for p in pts):
        return None
    if len({(p['x'], p['y']) for p in pts}) < 4:
        return None  # placeholder joints stacked on one point (fakes / unseen) - no real torso
    sx, sy = (pts[0]['x'] + pts[1]['x']) / 2, (pts[0]['y'] + pts[1]['y']) / 2
    hx, hy = (pts[2]['x'] + pts[3]['x']) / 2, (pts[2]['y'] + pts[3]['y']) / 2
    size = ((sx - hx) ** 2 + (sy - hy) ** 2) ** 0.5
    return (sx + hx) / 2, (sy + hy) / 2, size


def looks_spliced(frames, settle=5):
    '''True if the tracked body jumps (or changes size) between neighbouring
    frames AND stays at the new spot - a cut in the video, or the pose model
    switching to another person. A glitch that snaps back is ignored.'''
    pts = []
    for f in frames:
        t = _torso(f['landmarks']) if f['landmarks'] is not None else None
        if t is not None and t[2] > 0:
            pts.append((f['frame'], t))

    def median(vals):
        vals = sorted(vals)
        return vals[len(vals) // 2]

    def far(a, b, steps=1):
        dist = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 / b[2]
        return dist > SPLICE_JUMP * steps or max(a[2] / b[2], b[2] / a[2]) > SPLICE_SIZE_RATIO

    for k in range(1, len(pts) - settle):
        (f0, prev), (f1, new) = pts[k - 1], pts[k]
        if not far(new, prev, max(1, f1 - f0)):
            continue
        # where the body was before (median, so an earlier one-frame glitch doesn't count)
        before = [t for _, t in pts[max(0, k - settle):k]]
        was = tuple(median([t[i] for t in before]) for i in range(3))
        after = [t for _, t in pts[k + 1:k + 1 + settle]]
        stays = sum(not far(t, new) for t in after) >= settle - 1
        if stays and far(new, was):
            return True
    return False


def looks_rotated(frames):
    '''True if the body is mostly lying sideways in the image - usually a phone
    video whose rotation flag the decoder ignored.'''
    import math
    angles = []
    for f in frames:
        lm = f['landmarks']
        if lm is None or _torso(lm) is None:
            continue
        sx, sy = (lm[L_SHOULDER]['x'] + lm[R_SHOULDER]['x']) / 2, (lm[L_SHOULDER]['y'] + lm[R_SHOULDER]['y']) / 2
        hx, hy = (lm[L_HIP]['x'] + lm[R_HIP]['x']) / 2, (lm[L_HIP]['y'] + lm[R_HIP]['y']) / 2
        if (sx, sy) != (hx, hy):
            angles.append(abs(math.degrees(math.atan2(hx - sx, hy - sy))))  # 0 = upright
    if len(angles) < 10:
        return False
    angles.sort()
    return angles[len(angles) // 2] > MAX_TORSO_TILT


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

def _raw_release_frame(frames, angles, side):
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


def find_release_frame(frames, angles, side):
    '''
    frames: pose_extractor's result['frames']
    angles: elbow angle per frame, same order as frames (None if unknown),
            e.g. [a['elbow_angle'] for a in angles_for_video(frames)]
    side: 'left' or 'right' (shooting hand)
    returns (frame number, '') or (None, reason)

    Returns None with a reason instead of guessing when the footage can't be
    trusted: the tracked body jumps/changes (cut or another person), or the
    pose is missing for more than MAX_GAP_NEAR_RELEASE frames around the release.
    '''
    if looks_rotated(frames):
        return (None, REASON_ROTATED)
    if looks_spliced(frames):
        return (None, REASON_SPLICED)
    found, reason = _raw_release_frame(frames, angles, side)
    if found is None:
        return (None, reason)
    if missing_near(frames, found) > MAX_GAP_NEAR_RELEASE:
        return (None, REASON_POSE_LOST)
    return (found, '')
