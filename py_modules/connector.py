import socket
import json


def send_message(code, message, s):
    byte_message = code.to_bytes(4, 'little') + len(message).to_bytes(4, 'little') + bytes(message, 'utf-8')
    s.sendall(byte_message)
    action = int.from_bytes(s.recv(4), "little")
    data_bytes = bytearray()
    data_dict = ''
    if action == 0:
        length = int.from_bytes(s.recv(4), "little")
        while len(data_bytes) < length:
            packet = s.recv(length - len(data_bytes))
            data_bytes.extend(packet)
    else:
        return None
    data = data_bytes.decode('utf-8')
    if data != '':
        data_dict = json.loads(data)
    return data_dict


def get_map():
    server_addr = 'wgforge-srv.wargaming.net'
    server_port = 443
    server_address = (server_addr, server_port)

    # msg = b'{"name":"Boris"}'
    # msg = struct.pack('>I', len(msg)) + msg
    login_message = b'\x01\x00\x00\x00\x10\x00\x00\x00{"name":"User7"}'
    player_message = b'\x06\x00\x00\x00\x00\x00\x00\x00'
    first_layer_message = b'\n\x00\x00\x00\x0b\x00\x00\x00{"layer":0}'
    second_layer_message = b'\n\x00\x00\x00\x0b\x00\x00\x00{"layer":1}'
    game_message = b'\x07\x00\x00\x00\x00\x00\x00\x00'
    logout_message = b'\x02\x00\x00\x00\x00\x00\x00\x00'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)

    login_info = send_message(1, '{"name":"User7"}', s)
    player_info = send_message(6, '', s)
    game_info = send_message(7, '', s)
    first_layer_info = send_message(10, '{"layer":0}', s)
    second_layer_info = send_message(10, '{"layer":1}', s)

    return player_info, first_layer_info, second_layer_info, s


def get_info(s):
    turn_message = b'\x05\x00\x00\x00\x00\x00\x00\x00'

    second_layer_message = b'\n\x00\x00\x00\x0b\x00\x00\x00{"layer":1}'
    turn_message = send_message(5, '', s)

    game_info = send_message(10, '{"layer":1}', s)
    return game_info


def move_train(s, line_idx, speed, train_idx):
    message = '{"line_idx":%d,"speed":%d,"train_idx":%d}' % (line_idx, speed, train_idx)
    move = send_message(3, message, s)
    print(move)

def close_conn(s):
    s.close()