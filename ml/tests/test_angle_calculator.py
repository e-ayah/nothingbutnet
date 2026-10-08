from ml.angle_calculator import angles_for_frame

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
