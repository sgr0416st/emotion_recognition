import cv2
import time


cap = cv2.VideoCapture("outtest.mp4")
#fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fmt = cv2.VideoWriter_fourcc('M','J','P','G')

size = (640, 360)
fps = cap.get(cv2.CAP_PROP_FPS)

new_fps = 1

interval = int(fps/new_fps)

writer = cv2.VideoWriter('test_slice.avi', fmt, new_fps, size)

print("fps=", fps, "new_fps=", new_fps, "interval=", interval)
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    frame_num += 1
    if not ret:
        break

    frame = cv2.resize(frame, size)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    if frame_num % interval == 0:
        writer.write(frame)

writer.release()
cap.release()
cv2.destroyAllWindows()
