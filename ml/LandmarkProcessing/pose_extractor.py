import cv2		
import mediapipe as mp		

# extract_pose_from_video_smoothing: takes a video path and returns a list of dictionaries of the smoothed landmarks
# xtract_pose_from_video_no_smoothing: takes a video path and returns a list of dictionaries of the unprocessed landmarks
    
mp_pose = mp.solutions.pose		# imports the MediaPipe Pose Model
		
def extract_pose_from_video_smoothing(video_path):		
    cap = cv2.VideoCapture(video_path)		# opens a VideoCapture object using the video
    all_frame_data = []		
    previous_landmarks = None		
    frame_number = 0		
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:		# creates the pose object which has two requirements, a dection confidence for a person, and where is the new landmarks in new frame
        while cap.isOpened():		# keeps on looping until video is closed
            ret, frame = cap.read()		# takes each frame ret is False if end of video
            if not ret:		
                break		
            # MediaPipe needs RGB, OpenCV gives BGR		
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)		# converting from BGR to RGB
            results = pose.process(rgb_frame)		# runs the frame through the model
            if results.pose_landmarks:		# goes into the loop if there are successful pose detection elements
                h, w = frame.shape[:2]		# getting the height and width from the image
                # x, y in pixels for all 33 joints		
                current_landmarks = [		
                    {'x': lm.x * w, 'y': lm.y * h, 'visibility': lm.visibility}		
                    for lm in results.pose_landmarks.landmark		
                ]		
                # Temporal smoothing: alpha=0.7 means 70% current frame, 30% previous		
                if previous_landmarks is not None:		# Only doing Smoothing if there are previous landmarks
                    alpha = 0.7		
                    current_landmarks = [		
                        {'x': alpha * c['x'] + (1 - alpha) * p['x'],		# calculating the x value
                         'y': alpha * c['y'] + (1 - alpha) * p['y'],		# calculating the y value
                         'visibility': c['visibility']}		
                        for c, p in zip(current_landmarks, previous_landmarks)		# looping through current and previous detection for all 33 landmark locations
                    ]		
                previous_landmarks = current_landmarks		# moving the frames forward
                all_frame_data.append({'frame': frame_number, 'landmarks': current_landmarks})	# appending the frame and all the landmarks to the list	
            frame_number += 1		
    cap.release()		
    return all_frame_data		


def extract_pose_from_video_no_smoothing(video_path):		
    cap = cv2.VideoCapture(video_path)		# opens a VideoCapture object using the video
    all_frame_data = []				
    frame_number = 0		
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:		# creates the pose object which has two requirements, a dection confidence for a person, and where is the new landmarks in new frame
        while cap.isOpened():		# keeps on looping until video is closed
            ret, frame = cap.read()		# takes each frame ret is False if end of video
            if not ret:		
                break		
            # MediaPipe needs RGB, OpenCV gives BGR		
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)		# converting from BGR to RGB
            results = pose.process(rgb_frame)		# runs the frame through the model
            if results.pose_landmarks:		# goes into the loop if there are successful pose detection elements
                h, w = frame.shape[:2]		# getting the height and width from the image
                # x, y in pixels for all 33 joints		
                current_landmarks = [		
                    {'x': lm.x * w, 'y': lm.y * h, 'visibility': lm.visibility}		
                    for lm in results.pose_landmarks.landmark		
                ]		
                all_frame_data.append({'frame': frame_number, 'landmarks': current_landmarks})	# appending the frame and all the landmarks to the list	
            frame_number += 1		
    cap.release()		
    return all_frame_data		
