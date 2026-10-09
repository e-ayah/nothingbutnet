from ml.release_frame_detector import find_release_frame


def fake_frame(n, wrist_y, shoulder_y=300, side='right'):
    lm = [{'x': 0.0, 'y': 0.0, 'visibility': 1.0} for _ in range(33)]
    w, s = (16, 12) if side == 'right' else (15, 11)
    lm[w] = {'x': 400.0, 'y': float(wrist_y), 'visibility': 1.0}
    lm[s] = {'x': 300.0, 'y': float(shoulder_y), 'visibility': 1.0}
    return {'frame': n, 'landmarks': lm}


# elbow extends 8 degrees per frame, then stays straight (170) through the follow-through
# wrist goes above the shoulder (y < 300) from frame 11
SHOT_ANGLES = [min(60 + i * 8, 170) for i in range(30)]


def test_normal_shot():
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    frame, reason = find_release_frame(frames, SHOT_ANGLES, 'right')
    assert frame == 13  # first frame within 10 degrees of 170
    assert reason == ''


def test_follow_through_plateau_not_picked():
    # the biggest angle comes late in the follow-through - release should still be early
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    angles = list(SHOT_ANGLES)
    angles[28] = 175
    frame, reason = find_release_frame(frames, angles, 'right')
    assert frame == 14  # first frame within 10 degrees of 175
    assert reason == ''


def test_wrist_never_above_shoulder():
    frames = [fake_frame(i, 400 - i * 2) for i in range(30)]
    frame, reason = find_release_frame(frames, SHOT_ANGLES, 'right')
    assert frame is None
    assert reason == 'Wrist never goes above the shoulder'


def test_left_handed_shot():
    frames = [fake_frame(i, 400 - i * 10, side='left') for i in range(30)]
    frame, reason = find_release_frame(frames, SHOT_ANGLES, 'left')
    assert frame == 13
    assert reason == ''


def test_skips_missing_landmarks():
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    frames[13]['landmarks'] = None
    frame, reason = find_release_frame(frames, SHOT_ANGLES, 'right')
    assert frame == 14
    assert reason == ''


def test_skips_unseen_wrist():
    # pose_extractor gives x/y None for a joint it hasn't seen yet
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    frames[13]['landmarks'][16] = {'x': None, 'y': None, 'visibility': 0.1}
    frame, reason = find_release_frame(frames, SHOT_ANGLES, 'right')
    assert frame == 14
    assert reason == ''
