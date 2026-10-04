import numpy as np
from ml.testing.fakes import make_landmarks, make_shot


def calculate_angle(point_a, point_b, point_c):
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)

    vector_ba = a - b
    vector_bc = c - b

    cosine = np.dot(vector_ba, vector_bc) / (
        np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc)
    )

    cosine = np.clip(cosine, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine))

    return round(angle, 1)


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