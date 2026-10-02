cv2.VideoCapture() - manages inputs, outputs for video[creates a object belonging to cv2.VideoCapture class]
    Main Class Methods:
        .read() - grabs the next image frame and decodes it
            Returns True/False + matrix of pixels
        .isOpened() - checks for object successfully connected to webcam or videofile
            Returns True/False
            EX:
                cv2.VideoCapture('path_to_file')    Video File
                cv2.VideoCapture(0)     Webcam
        .released() - closes connection with file/camera
            Returns None

BGR => RGB
    BGR is an older color order (Blue Green Red) that was more efficient for older computer and what OpenCV was built on. Modern libraries like PyTorch, Tensorflow, MediaPipe Pose Landmark all use RGB

pose.process
    Input:
        Accepts a single image or video gram in the form of a 3D NumPy array
    Output:
        Returns a NamedTuple object which returns each point with an x, y coordinate, z, and visibility

x(0, 1)
    The x position of the point from 0 - 1 relative to the image

y(0, 1)
    The y position of the point from 0 - 1 relative to the image

visibility(0, 1)
    The confidence that the point is actually visible in the image


OPEN MEDIA PIPE LANDMARK DIAGRAM
Shoulders:
    11 - left shoulder
    12 - right shoulder
Elbows:
    13 - left elbow
    14 - right elbow
Wrists:
    15 - left wrist
    16 - right wrist
Hips:
    23 - left hip
    24 - right hip
Knees:
    25 - left knee
    26 - right knee
Ankles:
    27 - left ankle
    28 - right ankle


SMOOTHING FORMULA
formula: new = float * current + (1 - float) * previous
    the new position is the weighted average of the previous prediction step and the current predicted location
    if alpha/float is 1.0, the previous predictions do not matter and on the contrary, if it is 0.3, then the previous hold a lot of weight so the prediction location will be behind


SMOOTHING OPTIONS
Exponential Moving Average
    Description: Works recursively, meaning it gives the current frame a value while taking the previous value a certain value
    Formula = ax_t + (1 - a) x_(t + 1)
    Pros: Could be extremely Lag Tradeoff
    Cons: Fixes Jittering
Centered Moving Average
    Description: Takes a fixed group of value saround the current point and then averages them to find the point
    Formula = [x_(t - 1) + x_(t) + x_(t + 1)] / 3
    Pros: Extremely smooth and good at removing noice
    Cons: Not real time since it requires future precision
One Euro Filter
    Description: It is an adaptive low pass filter which changes the amount of smoothing depending on how quickly the movement is happening
    Formula a_t * x_t + (1 - a_t) * x_(t - 1) ~ Smoothing Algorithmn ~ where a_t = 1 / (1 + 1 / (2 * pi * f_(c, f) * T_e)) ~ Calculating How Much Smoothing ~ where f_(c, t) = f_(c) + B|derivative(x_t)| ~ Decides cutoff Frequency based on Speed ~
    Example: Fast Movement => Larger f_(c, t) => Larger a_t => Larger weight on current, less smoothing
    Pros: Smooths strongly when motion is slow and reduces smoothing when motion is fast - Adaptable
    Cons: Requires fine tuning of constant values 


RECOMMENDATION
Based on all the research and the requirements of the project, I would recommend the Centered Moving Average since our project utilizes a recording of a basketball player and then process it before returning advice/pose estimation requirements. If we were to build features that might require live camera pose detection/analysis, we could move towards a One Euro Fitler though that would require much more advanced testing and adjustment before it can be implemented. Based on the speed, scope, and resources for this project, I recommend using the Centered Moving Average.

