import cv2 as cv
import tempfile
import imageio_ffmpeg
import os
import subprocess

def encode_video(frames, fps, out_path):
    """
    Encodes a list of BGR frames into an H.264 MP4 video file

    What goes in (parameters):
        frames : numpy.ndarray
            A list of BGR images (NumPy arrays)
            All frames must be the same size
        fps: int or float
            The Frames Per Second of the output video
        out_path : str
            The final system file path where the encoded H.264 video will be written
    
    What comes out (Returns):
        None
            The output video is saved directly at out_path
    """
    if len(frames) == 0:
        raise ValueError("No frames to encode")

    height, width, channels = frames[0].shape

    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        fourcc = cv.VideoWriter.fourcc(*'mp4v')
        out = cv.VideoWriter(temp_path, fourcc, fps, (width, height))

        for frame in frames:
            out.write(frame)
        out.release()

        # -loglevel error: only print real problems (ffmpeg's normal output is ~40 lines per video)
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', temp_path, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out_path], check=True)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)