import numpy as np
import cv2


# video を録画、fpsの間引きを行うクラス
class VideoOperator:
    def __init__(self, fmt_str=('M', 'J', 'P', 'G'), org_path=0):
        self.cap = cv2.VideoCapture(org_path)
        self.fmt = cv2.VideoWriter_fourcc(fmt_str[0], fmt_str[1], fmt_str[2], fmt_str[3])
        self.cam_fps = self.cap.get(cv2.CAP_PROP_FPS)

    def _record(self, dst_path, record_fps=-1, size=(640, 360), func=None, func_data=None, show=False):
        if record_fps==-1:
            record_fps = self.cam_fps
        interval = int(self.cam_fps / record_fps)
        frame_num = 0

        writer = cv2.VideoWriter(dst_path, self.fmt, record_fps, size)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_num += 1
            if frame_num % interval == 0:
                frame = cv2.resize(frame, size)
                if func is not None:
                    func(frame, func_data)
                writer.write(frame)
                if show:
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(10) == 13:             # Enterキーで終了
                       break

        writer.release()
        if show:
            cv2.destroyAllWindows()

    def record(self, dst_path, record_fps=-1, size=(640, 360), func=None, func_data=None, show=False):
        if record_fps==-1:
            record_fps = self.cam_fps
        writer = cv2.VideoWriter(dst_path, self.fmt, record_fps, size)
        for frame in self.take(record_fps, size):
            if func is not None:
                func(frame, func_data)
            writer.write(frame)
            if show:
                cv2.imshow('frame', frame)
                if cv2.waitKey(10) == 13:  # Enterキーで終了
                    break

        writer.release()
        if show:
            cv2.destroyAllWindows()

    def take(self, record_fps=-1, size=(640, 360)):
        if record_fps == -1:
            record_fps = self.cam_fps
        interval = int(self.cam_fps / record_fps)
        frame_num = 0

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_num += 1
            if frame_num % interval == 0:
                frame = cv2.resize(frame, size)
                yield frame

    def close(self):
        self.cap.release()


##test用 画像サイズを表示するだけ
def callback_test(frame, func_data):
    print(np.shape(frame))


if __name__ == "__main__":
    dst = "../test_datas/test_video_org.avi"
    operator = VideoOperator()
    callback = callback_test
    operator.record(dst, func=callback)
    operator.close()

    dst_slice = "../test_datas/test_video_slice.avi"
    operator_2 = VideoOperator(org_path=dst)
    operator_2.record(dst_slice, record_fps=2)
    operator_2.close()
