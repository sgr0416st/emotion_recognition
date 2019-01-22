class Command:
    """
    リクエスト: [
        request_header: {
        request_size[2 byte], command[1 byte], data_number[1 byte]
        }(size: 4byte),
        params: {
        params1:(data_flag[1byte], data[n byte]), params2:(data_flag[1byte], data[n byte]), * * *
        }(size: request_size-4 byte)
    ]
    例外
    String_param:(data_flag[1 byte], data_size[2 byte], data[n byte])


    ・FLAG （後続バイナリのデータ型を識別）
    ・COM （コマンド）
    ・PC, SOTA の IPアドレス

    を保管
    逐次変更が必要
    """

    FLAG_BYTE = 1
    FLAG_SHORT = 2
    FLAG_INT = 4
    FLAG_DOUBLE = 8
    FLAG_STRING = 101

    COM_EXIT = 1
    COM_TEST = 2

    COM_NOD = 10
    COM_REJECT = 11
    COM_TILTS = 12

    COM_CONFUSE = 20
    COM_HAPPY = 21
    COM_SAD = 22
    COM_ANGRY = 23


    # 逐次変更が必要です
    MY_MAC_IP = "133.34.174.61"
    MY_WINDOWS_IP = "133.34.174.61"
    SOTA_IP = "133.34.174.81"
    PORT = 7777