import cv2
import time

def main():
    # dir = '/Users/satousuguru/workspace/programing/python' \
    #       '/emotion_recognition/samples/datas/video_audio_record_send_sample_data/'
    dir = "/Users/satousuguru/Movies/"
    name = "with_sota_kobayashi_cut"
    ext = '.mp4'
    new_ext = '.mp4'
    # fmt = cv2.VideoWriter_fourcc('M','J','P','G')
    fmt = cv2.VideoWriter_fourcc(*"mp4v")


    new_fps = 1
    cap = cv2.VideoCapture(dir + name + ext)
    size = (640, 360)
    fps = cap.get(cv2.CAP_PROP_FPS)

    interval = int(fps/new_fps)
    writer = cv2.VideoWriter(dir + name + "_slice" + new_ext, fmt, new_fps, size)

    print("fps=", fps, "new_fps=", new_fps, "interval=", interval)
    frame_num = 0

    while cap.isOpened():
        ret, frame = cap.read()
        frame_num += 1
        if not ret:
            break

        frame = cv2.resize(frame, size)
        # cv2.imshow("frame", frame)
        # cv2.waitKey(1)
        if frame_num % interval == 0:
            writer.write(frame)

    writer.release()
    cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    print("finish")
