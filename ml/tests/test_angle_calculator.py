from ml.angle_calculator import angles_for_frame, angles_for_video, calculate_angle, detect_shooting_side

def create_mock_test():
    mock_frame = []
    for i in range(33):
        mock_frame += [{'x': i * 0.01, 'y': i * 0.01, 'visibility': 1.0}] # multiply i * 0.01 so coordinates are spread out to avoid RuntimeWarning
    # 90° by default
    # 11/12 left/right shoulder · 13/14 elbow · 15/16 wrist · 23/24 hip · 25/26 knee · 27/28 ankle
    mock_frame[12] = {'x': 0.5, 'y': 0.5, 'visibility': 1.0} # shoulder
    mock_frame[14] = {'x': 0.5, 'y': 0.7, 'visibility': 1.0} # elbow
    mock_frame[16] = {'x': 0.7, 'y': 0.7, 'visibility': 1.0} # wrist
    return mock_frame

def test_90_degree_angle():
    frame = create_mock_test()
    result = angles_for_frame(frame, 'right')
    assert result['elbow_angle'] == 90.0

def test_180_degree_angle():
    frame = create_mock_test()
    frame[16] = {'x': 0.5, 'y': 0.9, 'visibility': 1.0} # move wrist so joints are in a straight line
    result = angles_for_frame(frame, 'right')
    assert result['elbow_angle'] == 180.0

def test_left_handed_shooter():
    frame = create_mock_test()
    # reset right joints
    frame[12] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    frame[14] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    frame[16] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    # create left-handed joints at 90° angle
    frame[11] = {'x': 0.5, 'y': 0.5, 'visibility': 1.0}
    frame[13] = {'x': 0.5, 'y': 0.7, 'visibility': 1.0}
    frame[15] = {'x': 0.7, 'y': 0.7, 'visibility': 1.0}
    result = angles_for_frame(frame, 'left')
    assert result['elbow_angle'] == 90.0

def test_missing_elbow():
    frame = create_mock_test()
    frame[14]['visibility'] = 0.1 # set visibility low enough to be unreliable
    result = angles_for_frame(frame, 'right')
    assert result['elbow_angle'] is None


def test_same_point_returns_none():
    # two joints at the same spot -> no angle instead of nan
    assert calculate_angle([1, 1], [1, 1], [2, 2]) is None

def test_video_with_no_person_frame():
    # pose_extractor gives landmarks=None when no person is found
    frame = create_mock_test()
    frame[15] = {'x': 0.1, 'y': 0.9, 'visibility': 1.0} # left wrist low so right side is picked
    frames = [{'frame': 0, 'landmarks': None}, {'frame': 1, 'landmarks': frame}]
    result = angles_for_video(frames)
    assert result[0]['elbow_angle'] is None
    assert result[1]['elbow_angle'] == 90.0

def test_side_detection_skips_unseen_wrist():
    # an unseen joint comes through as x/y None
    frame = create_mock_test()
    frame[15] = {'x': None, 'y': None, 'visibility': 0.1}
    assert detect_shooting_side([{'frame': 0, 'landmarks': frame}]) == 'right'
