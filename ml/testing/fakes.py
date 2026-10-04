def make_landmarks(points):
    # creates a list of 33 dictionaries for the pose landmarks
    landmarks = []

    for i in range(33):
        landmark = {
            "x": 0,
            "y": 0,
            "visibility": 1.0
        }
        if i in points:
            landmark["x"] = points[i][0]
            landmark["y"] = points[i][1]

        landmarks.append(landmark)
    return landmarks

def make_shot(n_frames, side='right'):
    #creates a sequence of fake basketball shot frames
    shots = []

    if side == 'left':
        shoulder = 11
        elbow = 13
        wrist = 15
    else:
        shoulder = 12
        elbow = 14
        wrist = 16

    for n in range(n_frames):
        progress = n / (n_frames - 1)

        wrist_y = 350 - 250 * progress
        elbow_x = 300 + 50 * progress
        elbow_y = 300 - 150 * progress

        points = {
            shoulder: (300, 200),
            elbow: (elbow_x, elbow_y),
            wrist: (350 + 100 * progress, wrist_y)
        }

        landmarks = make_landmarks(points)

        shots.append({
            "frame": n,
            "landmarks": landmarks
        })

    return shots
