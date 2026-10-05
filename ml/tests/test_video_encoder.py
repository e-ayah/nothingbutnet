import numpy as np
import os
import cv2 as cv
from ml.video_encoder import encode_video

def test_video_encoder():
    num_frames = 30
    fps = 30
    width, height = 200, 200
    out_path = "test_output.mp4"

    # creating mock frames of cyan 20 x 20 square moving diagonally across screen
    frames = []
    for i in range(num_frames):
        # 3 channels --> RGB
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        pos = i * 6
        frame[pos:pos + 20, pos:pos + 20] = [0, 255, 255]
        frames.append(frame)

    frames_array = np.array(frames)

    try:
        encode_video(frames_array, fps, out_path)
        assert os.path.exists(out_path), "Output file does not exist" # output exists
        assert os.path.getsize(out_path) > 0, "Output file is empty" # output isn't empty
        
        cap = cv.VideoCapture(out_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
        cap.release()

        assert frame_count == num_frames, f"Expected 30 frames but got {frame_count} frames"# output has 30 frames

    finally:
        if os.path.exists(out_path):
            os.remove(out_path)