import random
import socket
import time

from minecraft import protocol

with socket.socket() as sock:
    sock.connect(("2b2t.org", 25565))
    protocol.HandshakePacket("2b2t.org", 25565, 1).send(sock)
    protocol.StatusRequestPacket().send(sock)
    status_response = protocol.ResponsePacket.recv(sock).get_response()
    payload = random.getrandbits(64)
    t = time.time()
    protocol.PingPacket(payload).send(sock)
    if payload == protocol.ResponsePacket.recv(sock).get_payload():
        t = time.time() - t
        print(f"2b2t.org:25565\n==========\nPing: {t}\nServer info: {status_response}")
