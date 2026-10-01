from angle_calculator import angles_for_frame

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

def tests():
    print("---STARTING TESTS---")
    #Test 1 90° angle
    print("Test 1: 90°")
    frame1 = create_mock_test()
    result1 = angles_for_frame(frame1, 'right')
    if result1['elbow_angle'] == 90.0:
        print("Test 1: 90° --> PASSED")
    else:
        print("Test 1: 90° --> FAILED - Got:", result1['elbow_angle'])

    #Test 2 180° angle
    print("Test 2: 180°")
    frame2 = create_mock_test()
    frame2[16] = {'x': 0.5, 'y': 0.9, 'visibility': 1.0} # move wrist so joints are in a straight line
    result2 = angles_for_frame(frame2, 'right')
    if result2['elbow_angle'] == 180.0:
        print("Test 2: 180° --> PASSED")
    else:
        print("Test 2: 180° --> FAILED - Got:", result2['elbow_angle'])

    #Test 3 fake left-handed shooter
    print("Test 3: Left-handed Shooter")
    frame3 = create_mock_test()
    # reset right joints
    frame3[12] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    frame3[14] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    frame3[16] = {'x': 0.0, 'y': 0.0, 'visibility': 1.0}
    # create left-handed joints at 90° angle
    frame3[11] = {'x': 0.5, 'y': 0.5, 'visibility': 1.0}
    frame3[13] = {'x': 0.5, 'y': 0.7, 'visibility': 1.0}
    frame3[15] = {'x': 0.7, 'y': 0.7, 'visibility': 1.0}
    result3 = angles_for_frame(frame3, 'left')
    if result3['elbow_angle'] == 90.0:
        print("Test 3: Left-handed Shooter --> PASSED")
    else:
        print("Test 3: Left-handed Shooter --> FAILED - Got:", result3['elbow_angle'])

    #Test 4 missing elbow
    print("Test 4: Missing Elbow")
    frame4 = create_mock_test()
    frame4[14]['visibility'] = 0.1 # set visibility low enough to be unreliable
    result4 = angles_for_frame(frame4, 'right')
    if result4['elbow_angle'] == None:
        print("Test 4: Missing Elbow --> PASSED")
    else:
        print("Test 4: Missing Elbow --> FAILED - Got:", result4['elbow_angle'])

    print("---END OF TESTS---")

tests()