import sys
import cv2
 
path = sys.argv[1]
cap = cv2.VideoCapture(path)
frames = []
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frames.append(frame)
cap.release()
 
i = 0
while True:
    shown = frames[i].copy()
    cv2.putText(shown, f"frame {i} / {len(frames) - 1}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("frame viewer (a = back, d = next, q = quit)", shown)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        break
    if key == ord("d"):
        i = min(i + 1, len(frames) - 1)
    if key == ord("a"):
        i = max(i - 1, 0)
cv2.destroyAllWindows()
 
# run: python ml/tools/frame_viewer.py ~/clips/clip01.mp4
