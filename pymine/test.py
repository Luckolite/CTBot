import json
import socket
from pprint import pprint

from pymine.handshake import HandshakePacket
from pymine.packet import Packet
from pymine.status import StatusRequestPacket


class Wrapper:
    def __init__(self, sock):
        self.sock = sock

    def send(self, data):
        print(f'Sent data:     {data}')
        self.sock.send(data)

    def recv(self, count):
        data = self.sock.recv(count)
        print(f'Received data: {data}')
        return data


with socket.socket() as s:
    s.connect(("2b2t.org", 25565))
    # sock = Wrapper(s)
    sock = s

    HandshakePacket(protocol_version=340, server_address="2b2t.org", server_port=25565, next_state=1).send(sock)
    StatusRequestPacket().send(sock)
    status = Packet.recv(sock)
    pprint(json.loads(status.response))
