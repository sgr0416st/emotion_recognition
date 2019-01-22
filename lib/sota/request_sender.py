import socket
import struct

from lib.sota.command import Command


class RequestSender:
    """
    使い方
    1. requestSender オブジェクトを作成
    2. connect で 受信側（request_receiver）と接続
    3. 必要に応じて addParams を使い付加情報を書き込み
    4. set_request_header メソッドを使ってリクエストヘッダを作成する
    4. send メソッドを使って情報を送信
    5. 繰り返し使う場合は send の後に clear メソッドを使って情報をリセット
    6. 終了時に必ず close を呼び出して閉じる

    現在、int, double, String に対応
    """

    def __init__(self):
        print("RequestSender launch")
        self._request = None
        self._request_header = None
        self._params = []
        self._command = 0
        self._additional_data_number = 0
        self._params_data = None
        self._request_size = 0
        self._client = None
        self.clear()

    def connect(self, send_ip=Command.MY_MAC_IP, port=Command.PORT):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # オブジェクトの作成をします
        self._client.connect((send_ip, port))  # これでサーバーに接続します

    def clear(self):
        self._request = bytearray()
        self._request_header = bytearray()
        self._params.clear()
        self._command = 0
        self._additional_data_number = 0
        self._params_data = bytearray()
        self._request_size = 0

    def close(self):
        self._client.close()

    def send(self):
        self._make_request()
        request_length = len(self._request)
        total_sent = 0
        while total_sent < request_length:
            sent = self._client.send(self._request[total_sent:])
            if sent == 0:
                raise RuntimeError("Error")
            total_sent = total_sent + sent

    def set_request_header(self, command):
        self._request_size += 4
        request_size_data = self._request_size.to_bytes(2, 'little')
        self._command = command
        self._request_header.extend(request_size_data)
        self._request_header.append(command)
        self._request_header.append(self._additional_data_number)

    def _make_request(self):
        self._request.extend(self._request_header)
        self._request.extend(self._params_data)

    def add_param(self, data):
        param = bytearray()
        if isinstance(data, int):
            param.append(Command.FLAG_INT)
            param.extend(data.to_bytes(4, "little"))
            self._params.append(param)
            self._params_data.extend(param)
            self._request_size += 5
            self._additional_data_number += 1
        elif isinstance(data, float):
            param.append(Command.FLAG_DOUBLE)
            param.extend(struct.pack("<d", data))
            self._params.append(param)
            self._params_data.extend(param)
            self._request_size += 9
            self._additional_data_number += 1
        elif isinstance(data, str):
            param.append(Command.FLAG_STRING)
            data_str = data.encode("utf-8")
            size = 3 + len(data_str)
            size_data = size.to_bytes(2, "little")
            param.extend(size_data)
            param.extend(data_str)
            self._params.append(param)
            self._params_data.extend(param)
            self._request_size += size
            self._additional_data_number += 1

    def show_request(self):
        print("-------request-------")
        print("requestSize: " + str(self._request_size) + '\n'
              + "command: " + self.get_command_name(self._command) + '\n'
              + "addDataNumber: " + str(self._additional_data_number))
        for n in range(self._additional_data_number):
            param = self._params[n]
            print("param" + str(n) + ": " + str(self.get_param(param)))
        print("-------  end  -------")

    @staticmethod
    def get_command_name(command):
        if command == Command.COM_EXIT:
            name = "COM_EXIT"
        elif command == Command.COM_TEST:
            name = "COM_TEST"
        elif command == Command.COM_NOD:
            name = "COM_NOD"
        elif command == Command.COM_REJECT:
            name = "COM_REJECT"
        elif command == Command.COM_TILTS:
            name = "COM_TILTS"
        elif command == Command.COM_CONFUSE:
            name = "COM_CONFUSE"
        else:
            name = "undefined"
        return name

    @staticmethod
    def get_param(param):
        data_flag = param[0]
        if data_flag == Command.FLAG_INT:
            ans = 0
            del param[0]
            return ans.from_bytes(param, "little")
        elif data_flag == Command.FLAG_DOUBLE:
            del param[0]
            return struct.unpack("<d", param)[0]
        elif data_flag == Command.FLAG_STRING:
            del param[2]
            del param[1]
            del param[0]
            return param.decode("utf-8")
        else:
            print("undefined data flag")


if __name__ == '__main__':
    sender = RequestSender()
    #sender.connect(send_ip=Command.SOTA_IP)
    sender.connect()
    num1 = 21.435
    num2 = "abc"
    num3 = 4000
    num4 = "あいう"
    num5 = "えお"

    sender.add_param(num1)
    sender.add_param(num2)
    sender.add_param(num3)
    sender.add_param(num4)
    sender.add_param(num5)
    sender.set_request_header(Command.COM_TEST)
    sender.send()
    sender.show_request()
    sender.clear()
    sender.set_request_header(Command.COM_EXIT)
    sender.send()
    sender.show_request()
    sender.close()
