import cv2
def video_info(path):
    capture = cv2.VideoCapture(path)

    if not capture.isOpened():
        raise ValueError("Could not open video")

    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    duration_s = frame_count / fps

    capture.release()

    return {
        "fps": fps,
        "width": width,
        "height": height,
        "frame_count": frame_count,
        "duration_s": duration_s,
    }

def iter_frames(path):
    capture = cv2.VideoCapture(path)

    if not capture.isOpened():
        raise ValueError("Could not open video")
    try:
        frame_number = 0

        while True:
            success, frame = capture.read()

            if not success:
                break
            yield frame_number, frame
            frame_number += 1

    finally:
        capture.release()

def read_frames(path, max_frames=None):
    frames = []

    for frame_number, frame in iter_frames(path):
        frames.append(frame)

        if max_frames is not None and len(frames) >= max_frames:
            break


    return frames