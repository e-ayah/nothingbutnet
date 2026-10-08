import os
import cv2
import pytest
from ml.pose_extractor import extract_pose

CLIP = os.path.join(os.path.dirname(__file__), "data", "pose_clip.mp4")

@pytest.fixture(scope="module")
def result() -> dict:
    '''
    runs extract_pose() from nothingbutnet/ml/pose_extractor on CLIP
    '''
    return extract_pose(CLIP)

#TESTS:
def test_one_entry_per_frame(result):
    '''
    tests that every frame has an entry
    '''
    assert len(result['frames']) == result['frame_count']

def test_33_landmarks_when_person(result):
    '''
    tests that every frame with a person has exactly 33 joints
    '''
    for f in result['frames']:
        if f['landmarks'] is not None:
            assert len(f['landmarks']) == 33

def test_fps_positive(result):
    '''
    tests that fps was read from the video
    '''
    assert result['fps'] > 0

def test_size_matches_clip(result):
    '''
    tests that width and height matches the clip's real size
    '''
    cap = cv2.VideoCapture(CLIP)
    assert result['width'] == int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    assert result['height'] == int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()