# -*- coding: utf-8 -*-
import numpy as np
import cv2
import json
import time


from lib.my_face_api import MyFaceAPI


def record_emotion_from_video(video_path, record_path):
    # video recognize
    results = []
    recognizer = MyFaceAPI(local_file_mode=True)
    cap = cv2.VideoCapture(video_path)
    counter = 0
    ImagePerMinute = 20

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            counter += 1
            print(counter)
            if counter%ImagePerMinute == 0:
                print("sleep...")
                time.sleep(60)

            recognizer.read(mat_image=frame)
            dict = recognizer.recognize()['emotion']
            print(json.dumps(dict, indent=4))
            results.append(dict)
        else:
            break

    cap.release()

    # json to csv
    # jsonのキー一覧を取得（jsonData[0]のところだけ）
    json_key = list(results[0].keys())
    csv_result = ""

    # csvヘッダ行作成
    for i, key in enumerate(json_key):
        if i < len(json_key) - 1:
            csv_result = csv_result + '"' + key + '"' + ','
        elif i == len(json_key) - 1:
            csv_result = csv_result + '"' + key + '"' + '\n'

    # データ部分を作成
    for i, value in enumerate(results):
        for ii, key in enumerate(json_key):
            if ii < len(json_key) - 1:
                if key in value:
                    csv_result = csv_result + '"' + str(value[key]) + '",'
                else:
                    csv_result = csv_result + '"",'
            elif ii == len(json_key) - 1:
                if key in value:
                    csv_result = csv_result + '"' + str(value[key]) + '"\n'
                else:
                    csv_result = csv_result + '""\n'

    with open(record_path, mode='w') as f:
        f.write(csv_result)


if __name__ == '__main__':
    # video_p = "/Users/satousuguru/workspace/programing/python/emotion_recognition/test_datas/sample_video.mov"
    # record_p = '../datas/emotion_record_sample_data/test.csv'
    name = 'zyo'
    dir = "/Users/satousuguru/Movies/"

    video_name = 'with_sota_' + name + '_cut_slice.mp4'
    video_p = dir + video_name
    record_p = dir + 'with_sota_' + name + '_cut_slice.csv'

    record_emotion_from_video(video_p, record_p)

    with open(record_p) as f:
        print(f.read())
