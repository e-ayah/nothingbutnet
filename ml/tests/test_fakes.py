from ml.angle_calculator import calculate_angle
from ml.testing.fakes import make_landmarks, make_shot


def test_make_landmarks():
    landmarks = make_landmarks({
        12: (300, 200),
        14: (300, 300),
        16: (400, 300)
    })

    angle = calculate_angle(
        (landmarks[12]["x"], landmarks[12]["y"]),
        (landmarks[14]["x"], landmarks[14]["y"]),
        (landmarks[16]["x"], landmarks[16]["y"])
    )

    assert angle == 90.0
    assert len(landmarks) == 33


def test_make_shot_left():
    shots = make_shot(30, 'left')

    first_wrist = shots[0]["landmarks"][15]
    last_wrist = shots[29]["landmarks"][15]

    assert last_wrist["y"] < first_wrist["y"]

def test_make_shot_works_with_real_pipeline():
    # the fakes are shared test data, so they must work with the real ML code
    from ml.angle_calculator import angles_for_video, detect_shooting_side
    from ml.release_frame_detector import find_release_frame
    for side in ('right', 'left'):
        shots = make_shot(30, side)
        assert detect_shooting_side(shots) == side
        elbows = [a['elbow_angle'] for a in angles_for_video(shots)]
        assert elbows[-1] > elbows[0]  # arm extends during the shot
        frame, reason = find_release_frame(shots, elbows, side)
        assert frame is not None


def test_make_shot_single_frame():
    assert len(make_shot(1)) == 1
