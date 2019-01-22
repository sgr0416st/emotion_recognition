import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
size = (640, 360)
fps = cap.get(cv2.CAP_PROP_FPS)


writer = cv2.VideoWriter('outtest.mp4', fmt, fps, size)

print("fps=", fps)
frame_num = 0
start_video_time = time.time()

while True:
    start = time.time()
    _, frame = cap.read()
    frame_num += 1
    frame = cv2.resize(frame, size)
    writer.write(frame)
    cv2.imshow('frame', frame)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # Enterキーで終了
    if cv2.waitKey(10) == 13:
        break

video_time = time.time() - start_video_time
estimated_fps = frame_num / video_time
print("frame_num=", frame_num, "video_time=", video_time, "estimated_fps=", estimated_fps)
# 保存
writer.release()
cap.release()
cv2.destroyAllWindows()