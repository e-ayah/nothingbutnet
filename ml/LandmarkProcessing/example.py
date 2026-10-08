from pose_extractor import extract_pose_from_video_smoothing, extract_pose_from_video_no_smoothing
import csv
import os

VIDEO_LOCATION = "first_5_seconds.mp4"

# paths are relative to this file, so it runs from any folder
file_path = os.path.dirname(os.path.abspath(__file__))

# the clip isn't committed (videos are gitignored) - put your own copy here
video_path = os.path.join(file_path, VIDEO_LOCATION)
if not os.path.exists(video_path):
    raise SystemExit(f"No video at {video_path} - add a local clip named {VIDEO_LOCATION}")

landmark_data_smooth = extract_pose_from_video_smoothing(video_path)
landmark_data_no_smooth = extract_pose_from_video_no_smoothing(video_path)

with open(os.path.join(file_path, "landmarksSmooth.csv"), "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow(["frame", "landmark", "x", "y", "visibility"])

    for frame_data in landmark_data_smooth:
        frame = frame_data["frame"]

        for landmark_number, landmark in enumerate(frame_data["landmarks"]):
            writer.writerow([
                frame,
                landmark_number,
                landmark["x"],
                landmark["y"],
                landmark["visibility"]
            ])

with open(os.path.join(file_path, "landmarksNoSmooth.csv"), "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow(["frame", "landmark", "x", "y", "visibility"])

    for frame_data in landmark_data_no_smooth:
        frame = frame_data["frame"]

        for landmark_number, landmark in enumerate(frame_data["landmarks"]):
            writer.writerow([
                frame,
                landmark_number,
                landmark["x"],
                landmark["y"],
                landmark["visibility"]
            ])



print(len(landmark_data_smooth))

print(landmark_data_smooth[0]['landmarks'][0])

