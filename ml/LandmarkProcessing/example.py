from pose_extractor import extract_pose_from_video_smoothing, extract_pose_from_video_no_smoothing
import csv
import os

VIDEO_LOCATION = "first_5_seconds.mp4"

video_path = os.path.join(os.getcwd(), "nothingbutnet", "ml", "LandmarkProcessing", VIDEO_LOCATION)

file_path = os.path.join(os.getcwd(), "nothingbutnet", "ml", "LandmarkProcessing")

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

