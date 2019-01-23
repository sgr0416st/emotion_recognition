import http.client, urllib.request, urllib.parse, urllib.error, base64, cv2
import json

# microsoft APIを用いて感情認識を行うクラ
# 手順：init -> read -> recognizde
class MyFaceAPI():
    # 指定したパラメータを元に、Request headers、Request parametersを設定する
    def __init__(self, parameters='emotion', local_file_mode=True):
        self.body = None
        self.local_file_mode = local_file_mode
        if self.local_file_mode:
            _type = 'application/octet-stream'
        else:
            _type = 'application/json'

        #### Request headers
        # 'Content-Type': APIに送るメディアのタイプ.
        # 'application/json'(URL指定の場合),
        # 'application/octet-stream' (Local ファイル転送の場合)
        # 'Ocp-Apim-Subscription-Key': APIキーを指定する
        self.headers = {
            # Request headers
            'Content-Type': _type,
            'Ocp-Apim-Subscription-Key': '207dfa0ead184154ad9a427c0c9c5d3f',
        }

        #### Request parameters
        # 取得したい情報について、パラメータを指定する
        # 'returnFaceId': 入力した顔画像に付与されるIDを返すかどうか
        # 'returnFaceLandmarks' : 目や口などの特徴となる部分の座標を返すかどうか
        # 'returnFaceAttributes' :　認識した顔からわかる属性を返す
        #   指定できるパラメータは以下で、コンマで分けて複数指定可能
        #       age, gender, headPose, smile, facialHair,
        #       glasses, emotion, hair, makeup, occlusion,
        #       accessories, blur, exposure and noise
        self.params = urllib.parse.urlencode({
            'returnFaceId': 'false',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': parameters
        })

    # 指定したパラメータを元に、Request bodyを設定する
    def read(self, file_path=None, url=None, mat_image=None):
        #### Request body
        # 入力したい画像の指定をする. 画像URLの指定, local ファイルの指定から選択
        # 画像はJPEG, PNG, GIF, BMPに対応
        # サイズの上限は4MB
        # 認識可能な顔のサイズは 36x36 - 4096x4096 pixelsの範囲
        # 最大64個の顔を認識可能
        if file_path is not None:
            ## Local file指定の場合
            # 以下の image_file_path に読み込むファイルのパスを指定する
            with open(file_path, 'rb') as image_file:
                self.body = image_file.read()
        elif url is not None:
            ## URL 指定の場合
            # file_pathは画像のURLを指定する
            _file = {'url': file_path}
            self.body = json.dumps(_file)
        elif mat_image is not None:
            _, buffer = cv2.imencode('.jpg', mat_image)
            self.body = buffer.tobytes()

    def recognize(self):
        emotion_dict = {"emotion": {}}
        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/detect?%s" % self.params, self.body, self.headers)
            response = conn.getresponse()
            data = json.loads(response.read())
            if len(data) > 0:
                if 'message' in data:
                    print(data['message'])
                elif 'faceAttributes' in data[0]:
                    emotion_dict = data[0].get('faceAttributes')
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        return emotion_dict


if __name__ == '__main__':
    path = '/Users/satousuguru/workspace/programing/python/emotion_recognition/test_datas/free_face.jpeg'
    # path = '/Users/satousuguru/workspace/programing/python/emotion_recognition/test_datas/OculusDK2.JPG'
    recognizer = MyFaceAPI(local_file_mode=True)
    recognizer.read(file_path=path)
    dict = recognizer.recognize()
    print(json.dumps(dict, indent=4))
