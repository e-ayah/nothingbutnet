'''
pose extractor

structure: dict (result) -> list (frames) -> dict (one frame) -> list (landmarks) -> dict (one joint)
output format of extract_pose(): dict
{
    'fps': float                     | frames per second of the video
    'width': int                     | frame width in px
    'height': int                    | frame height in px
    'frame_count': int               | number of frames read
    'frames': list
    [
        {
            'frame': int             | frame index (starting from 0)
            'landmarks': list        | 33* of MediaPipe joints; None if no person found
            [
                {
                'x': float or None   | px position
                'y': float or None   | px position (increases downwards)
                'visibility': float  | 0->1; measures MediaPipe's confidence that the joint is visible
                'reliable': bool     | False if visibility<min_visibility
                }
            ]*33 or None
        }
    ]
}
'''

import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose

def extract_pose(video_path: str, min_visibility: float=0.5, alpha: float=0.7) -> dict:
    '''
    runs MediaPipe Pose on every frame of a video
    '''
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    all_frame_data = [] #list of dicts -> collect every frame's results
    previous_landmarks = None #last frame's 33 joints
    frame_number = 0 #index of current frame

    with mp_pose.Pose(min_detection_confidence=0.5, #only accept person found with >=50% confidence
                      min_tracking_confidence=0.5) as pose: #redetect when tracking drops below 50%
        while cap.isOpened():
            ret, frame = cap.read() #reading capture -> ret is True if frame was grabbed; frame is BGR image array in shape (height,width,3)
            if not ret:
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #run pose model on current frame (we need RGB so we converted BGR->RGB)
            if(results.pose_landmarks is None):
                all_frame_data.append({'frame': frame_number,
                                       'landmarks': None})
            else:
                h,w = frame.shape[:2] #height & width in px
                #MediaPipe returns 33 joints with x & y as 0-1 fractions; * size = px
                current_landmarks = [{'x': lm.x*w,
                                      'y': lm.y*h,
                                      'visibility': lm.visibility}
                                      for lm in results.pose_landmarks.landmark] #loops through 33 joints in fixed order -> https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker
                landmarks = []
                for i, c in enumerate(current_landmarks):
                    p = previous_landmarks[i] if previous_landmarks is not None else None
                    has_prev = p is not None and p['x'] is not None
                    #checks & flags visibility confidence level & reliability
                    if(c['visibility'] < min_visibility):
                        x = p['x'] if has_prev else None
                        y = p['y'] if has_prev else None
                        reliable = False
                    elif(has_prev):
                        #smoothing -> reduces frame to frame jitter
                        #new = alpha*current + (1-alpha)*previous
                        x = alpha*c['x'] + (1-alpha)*p['x']
                        y = alpha*c['y'] + (1-alpha)*p['y']
                        reliable = True
                    else:
                        x, y = c['x'], c['y']
                        reliable = True
                    landmarks.append({
                        'x': x,
                        'y': y,
                        'visibility': c['visibility'],
                        'reliable': reliable
                    })
                previous_landmarks = landmarks
                all_frame_data.append({'frame': frame_number,
                                       'landmarks': landmarks})
            frame_number += 1
        cap.release() #close video file
        return {
            'fps': fps,
            'width': width,
            'height': height,
            'frame_count': frame_number,
            'frames': all_frame_data
        }