import numpy as np

from ml.angle_labels import draw_angle_labels
from ml.skeleton_overlay import draw_skeleton
from ml.testing.fakes import make_shot

ANGLES = {'elbow_angle': 150.0, 'knee_angle': 165.0, 'shoulder_angle': 60.0}


def blank_frame(width=480, height=852):
    return np.zeros((height, width, 3), np.uint8)


def test_skeleton_draws_on_frame():
    landmarks = make_shot(30)[29]['landmarks']
    frame = draw_skeleton(blank_frame(), landmarks, {'elbow_alignment': 'needs_work'}, 'right')
    assert frame.any()  # something was drawn


def test_labels_draw_on_frame():
    landmarks = make_shot(30)[29]['landmarks']
    frame = draw_angle_labels(blank_frame(), landmarks, ANGLES, 'right')
    assert frame.any()


def test_no_person_frame_is_unchanged():
    # pose_extractor gives landmarks=None when no person is found
    frame = draw_skeleton(blank_frame(), None, {}, 'right')
    frame = draw_angle_labels(frame, None, ANGLES, 'right')
    assert not frame.any()


def test_unseen_joint_is_skipped():
    # an unseen joint comes through as x/y None
    landmarks = make_shot(30)[29]['landmarks']
    landmarks[14] = {'x': None, 'y': None, 'visibility': 0.1}
    draw_skeleton(blank_frame(), landmarks, {}, 'right')
    draw_angle_labels(blank_frame(), landmarks, ANGLES, 'right')
