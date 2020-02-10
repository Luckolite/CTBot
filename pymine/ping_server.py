import json
import random
import socket
import time

from pymine.packets import packet, status, handshake


def ping(address, port=25565):
    with socket.socket() as sock:
        sock.connect((address, port))

        # Handshake to initiate connection
        handshake.HandshakePacket(
            protocol_version=340, server_address=address, server_port=port, next_state=1
        ).send(sock)

        packet.state = 1

        # Request status
        status.StatusRequestPacket().send(sock)

        # Receive status
        response = json.loads(packet.Packet.recv(sock).response)

        # Generate random bits (ping payload)
        payload = random.getrandbits(64)
        if payload & 0x8000000000000000:
            payload -= 0x10000000000000000

        t = time.time()
        # Ping
        status.PingPacket(
            payload=payload
        ).send(sock)

        # Pong
        pong = packet.Packet.recv(sock)
        t = (time.time() - t) * 1000
        if pong.payload != payload:
            print("Invalid payload")

        response['ping'] = t
        return response
