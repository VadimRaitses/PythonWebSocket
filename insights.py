import datetime
import socket
import threading
import struct
from hashlib import sha1
from base64 import b64encode
import sys
import re
import json


class Client:
    id = 0
    address = None
    is_hand_shaken = False
    isConnected = False

    def __init__(self, address):
        Client.id += 1
        self.address = address
        self.is_hand_shaken = True
        self.isConnected = True


class MyServer:
    __doc__ = "instance of my customized web socket server"
    clients_dictionary = {}
    server_port = 0
    server_running_status = False
    handshake_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    server_socket = None
    server_host = None
    server_ip = None
    server_web_socket_answer = ('HTTP/1.1 101 Switching Protocols',
                                                    'Upgrade: websocket',
                                                    'Connection: Upgrade',
                                                    'Sec-WebSocket-Accept: {key}\r\n\r\n',)

    STREAM = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA

    def __init__(self, port):
        self.clients_dictionary = {}
        self.server_port = port

    def run(self):
        self.server_running_status = True
        print('Starting a Socket Server...')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = socket.gethostname()
        self.server_ip = socket.gethostbyname(self.server_host)
        print("Host name {} : {} : {}...".format(self.server_ip
                                                 , self.server_host
                                                 , self.server_port))
        self.server_socket.bind(("", self.server_port))
        self.server_socket.listen(5)
        while self.server_running_status:
            c, client_address = self.server_socket.accept()
            print('Got connection from', client_address)
            threading.Thread(target=self.do_handshake, args=(c, client_address)).start()

    def do_handshake(self, c, client_address):
        print('Do Handshake')
        if client_address not in self.clients_dictionary:
            text = c.recv(1024)
            client_msg = text.decode("utf-8")
            print(text)
            key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', client_msg)
                   .groups()[0]
                   .strip())
            k = sha1((key + self.handshake_GUID).encode("utf-8")).digest()
            response_key = b64encode(k)
            response = '\r\n'\
                .join(self.server_web_socket_answer)\
                .format(key=response_key)\
                .replace("b'", "")\
                .replace("'", "")
            print(response)
            c.sendto(response.encode("utf-8"), client_address)
            user = Client(client_address)
            self.clients_dictionary[client_address] = user
            self.interchange(c, client_address)
        else:
            self.interchange(c, client_address)

    def interchange(self, c, client_address):
        lock = threading.Lock()
        lock.acquire()
        while 1:
            print("Waiting for data from", client_address)
            data = c.recv(1024)
            data_length = data[1] & 127
            index_mask = 2
            if data_length == 126:
                index_mask = 4
            elif data_length == 127:
                index_mask = 10

            masks = [m for m in data[index_mask: index_mask + 4]]
            index_first_data_byte = index_mask + 4
            decoded_chars = []
            i = index_first_data_byte
            j = 0
            while i < len(data):
                decoded_chars.append(chr(data[i] ^ masks[j % 4]))
                i += 1
                j += 1
            # print("Done", len(data))

            if not data:
                print("No data")
                break
            json_message = ''.join(decoded_chars)
            print('Data from', client_address, ':', json_message)
            try:
                json_object = json.loads(json_message)
                self.send_message(c, json_object)
                #  break
            except Exception:
                print("Something bad happened")
                sys.exit(1)
                lock.release()

    def send_message(self, client, data):

        data = json.dumps(data, sort_keys=True)
        # Empty message to start with
        message = ""
        # s = "Hello"
        # always send an entire message as one frame (fin)
        b1 = 0x80

        # in Python 2, strs are bytes and unicodes are strings
        if type(data) == str:
            b1 |= self.TEXT
            payload = data.encode("UTF8")

        elif type(data) == bytes:
            b1 |= self.TEXT
            payload = data

        # Append 'FIN' flag to the message
        message += chr(b1)

        # never mask frames from the server to the client
        b2 = 0

        # How long is our payload?
        length = len(payload)
        if length < 126:
            b2 |= length
            message += chr(b2)

        elif length < (2 ** 16) - 1:
            b2 |= 126
            message += chr(b2)
            l = struct.pack(">H", length)
            message += l

        else:
            l = struct.pack(">Q", length)
            b2 |= 127
            message += chr(b2)
            message += l

        # Append payload to message
        message += data
        # string.encode(utf-8) method , put junk byte in the start of byte array
        # and instead proper masking bit you get wrong bit from junk byte passed by string.encode()
        # so i decided remove this byte by using del from byte array
        a = bytearray(message, 'utf-8')
        del a[0:1]
        client.send(a)

server = MyServer(12345)
server.run()
