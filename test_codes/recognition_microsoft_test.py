import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

#### Request headers
#'Content-Type': APIに送るメディアのタイプ.
#  'application/json'(URL指定の場合), 'application/octet-stream' (Local ファイル転送の場合)
#'Ocp-Apim-Subscription-Key': APIキーを指定する
headers = {
    # Request headers
    # 'Content-Type': 'application/json',
    'Content-Type': 'application/octet-stream',
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
params = urllib.parse.urlencode({
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
})

#### Request body
# 入力したい画像の指定をする. 画像URLの指定, local ファイルの指定から選択
# 画像はJPEG, PNG, GIF, BMPに対応
# サイズの上限は4MB
# 認識可能な顔のサイズは 36x36 - 4096x4096 pixelsの範囲
# 最大64個の顔を認識可能

## URL 指定の場合以下のコメントアウトを外すし、image_urlを指定する
# image_url = 'https://XXXXX'
# body = { 'url': image_url }
# body = json.dumps(body)

## Local file指定の場合
# 以下の image_file_path に読み込むファイルのパスを指定する
with open('/Users/satousuguru/workspace/programing/python/emotion_recognition/test_datas/free_face.jpeg', 'rb') as image_file:
    body = image_file.read()

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    print(json.dumps(data, indent=4))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################