import socket
import threading
import struct
from hashlib import sha1
from base64 import b64encode
import sys
import re
import datetime


STREAM = 0x0
TEXT = 0x1
BINARY = 0x2
CLOSE = 0x8
PING = 0x9
PONG = 0xA


FIN = 0
HEADERB1 = 1
HEADERB2 = 3
LENGTHSHORT = 4
LENGTHLONG = 5
MASK = 6
PAYLOAD = 7

MAXHEADER = 65536
MAXPAYLOAD = 33554432

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
clients = {}


def start_server(port):
    print("Starting a Socket Server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    ip = socket.gethostbyname(host)
    port = port  # Reserve a port for your service.
    print("Host name {} : {} : {}...".format(ip, host, port))
    s.bind(("", port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        # s.connect(addr)
        print('Got connection from', addr)
        clients[addr] = c
        threading.Thread(target=make_handshake, args=(c, addr)).start()

def serve_client(c, client_address):


    print("datetime {0}".format(datetime.datetime.now().time()))



def make_handshake(c, addr):
    data = ""
    websocket_answer = ('HTTP/1.1 101 Switching Protocols',
                        'Upgrade: websocket',
                        'Connection: Upgrade',
                        'Sec-WebSocket-Accept: {key}\r\n\r\n',)

    text = c.recv(1024)
    clientstring_msg = text.decode("utf-8")
    print(text)
    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', clientstring_msg)
           .groups()[0]
           .strip())
    k = sha1((key + GUID).encode("utf-8")).digest()  # (sha1(key + GUID).digest()).encode("utf-8")
    response_key = b64encode(k)
    response = '\r\n'.join(websocket_answer).format(key=response_key).replace("b'", "").replace("'", "")
    # str = "Content-Type: text/plain;charset=utf-8"
    print(response)
    # bytes = websocket_answer.encode("utf-8")
    c.sendto(response.encode("utf-8"), addr)

    lock = threading.Lock()
    # lock.acquire()
    while 1:
        print("Waiting for data from", addr)
        data = c.recv(1024)

        # byteArray = [ord(character) for character in data]
        datalength = data[1] & 127
        indexFirstMask = 2
        if datalength == 126:
            indexFirstMask = 4
        elif datalength == 127:
            indexFirstMask = 10

        masks = [m for m in data[indexFirstMask: indexFirstMask + 4]]
        indexFirstDataByte = indexFirstMask + 4
        decodedChars = []
        i = indexFirstDataByte
        j = 0
        while i < len(data):
            decodedChars.append(chr(data[i] ^ masks[j % 4]))
            i += 1
            j += 1
        print("Done", len(data))
        print(decodedChars)

        if not data:
            print("No data")
        break

    print('Data from', addr, ':', decodedChars)

    try:
        sendMessage("Hello", c, data)
    except Exception:
        print("Something bad happened")
        sys.exit(1)
        lock.release()




# c.sendto("vafasdsadas".encode("utf-8"),addr)
# del clients[addr]
# c.close()
# print('Client closed:', addr)
# lock.release()


def sendMessage(s, client, data):
    """
    Encode and send a WebSocket message
    """

    # Empty message to start with
    message = ""
    s = "Hello"
    # always send an entire message as one frame (fin)
    b1 = 0x80

    # in Python 2, strs are bytes and unicodes are strings
    if type(s) == str:
        b1 |= TEXT
        payload = s.encode("UTF8")

    elif type(s) == bytes:
        b1 |= TEXT
        payload = s

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
    # "\x81\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58"#"
    # message+=payload#.decode() "\x48\x65\x6c\x6c\x6f" #
    # str.encode(message)
    # ':'.join(hex(ord(x))[2:] for x in 'Hello World!')
    # Send to the client

    client.send(b'\x81\x05Hello')


start_server(12345)
