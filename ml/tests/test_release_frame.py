import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from release_frame_detector import find_release_frame


def fake_frame(n, wrist_y, shoulder_y=300, side='right'):
    lm = [{'x': 0.0, 'y': 0.0, 'visibility': 1.0} for _ in range(33)]
    w, s = (16, 12) if side == 'right' else (15, 11)
    lm[w] = {'x': 400.0, 'y': float(wrist_y), 'visibility': 1.0}
    lm[s] = {'x': 300.0, 'y': float(shoulder_y), 'visibility': 1.0}
    return {'frame': n, 'landmarks': lm}


def test_normal_shot():
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    angles = [60 + i * 4 for i in range(30)]
    frame, reason = find_release_frame(frames, angles, 'right')
    assert frame == 29
    assert reason == ''


def test_wrist_never_above_shoulder():
    frames = [fake_frame(i, 400 - i * 2) for i in range(30)]
    angles = [60 + i * 4 for i in range(30)]
    frame, reason = find_release_frame(frames, angles, 'right')
    assert frame is None
    assert reason == 'Wrist never goes above the shoulder'


def test_left_handed_shot():
    frames = [fake_frame(i, 400 - i * 10, side='left') for i in range(30)]
    angles = [60 + i * 4 for i in range(30)]
    frame, reason = find_release_frame(frames, angles, 'left')
    assert frame == 29
    assert reason == ''


def test_skips_missing_landmarks():
    frames = [fake_frame(i, 400 - i * 10) for i in range(30)]
    frames[29]['landmarks'] = None
    angles = [60 + i * 4 for i in range(30)]
    frame, reason = find_release_frame(frames, angles, 'right')
    assert frame == 28
    assert reason == ''