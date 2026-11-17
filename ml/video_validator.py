import math

import cv2
import mediapipe as mp
import numpy as np


MAX_SECONDS = 15
MIN_BRIGHTNESS = 40
SAMPLES = 10
MIN_POSE_FRAMES = 3
MAX_SAMPLE_SIDE = 640

UNREADABLE_VIDEO = "We couldn't read this video. Try exporting it as an MP4."


def validate(path: str) -> tuple[bool, str | None]:
    """Return (True, None) for a usable clip or (False, reason) otherwise."""
    cap = cv2.VideoCapture(str(path))
    frames: list[np.ndarray] = []
    total_brightness = 0.0

    try:
        if not cap.isOpened():
            return False, UNREADABLE_VIDEO

        fps = cap.get(cv2.CAP_PROP_FPS)
        reported_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if (
            not math.isfinite(fps)
            or fps <= 0
            or not math.isfinite(reported_count)
            or reported_count < 1
        ):
            return False, UNREADABLE_VIDEO

        frame_count = int(reported_count)
        if frame_count / fps > MAX_SECONDS:
            return False, "This video is too long. Trim it to 15 seconds or less."

        sample_indices = np.linspace(
            0, frame_count - 1, num=min(SAMPLES, frame_count), dtype=int
        )

        for index in sample_indices:
            if not cap.set(cv2.CAP_PROP_POS_FRAMES, int(index)):
                continue

            ok, frame = cap.read()
            if not ok or frame is None:
                continue

            height, width = frame.shape[:2]
            longest_side = max(height, width)
            if longest_side > MAX_SAMPLE_SIDE:
                scale = MAX_SAMPLE_SIDE / longest_side
                frame = cv2.resize(
                    frame,
                    (max(1, round(width * scale)), max(1, round(height * scale))),
                    interpolation=cv2.INTER_AREA,
                )

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            total_brightness += float(gray.mean())
            frames.append(frame)
    finally:
        cap.release()

    if not frames:
        return False, UNREADABLE_VIDEO

    if total_brightness / len(frames) < MIN_BRIGHTNESS:
        return False, "This video is too dark. Try filming in better light."

    pose_frames = 0
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1) as pose:
        for frame in frames:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if pose.process(rgb).pose_landmarks is not None:
                pose_frames += 1
                if pose_frames >= MIN_POSE_FRAMES:
                    return True, None

    return False, "We couldn't find a person. Film from the side with your whole body in view."