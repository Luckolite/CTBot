import random
import socket
import time

from pymine.packets import packet, handshake, status


class Client:
    def __init__(self, address, port=25565):
        self.address = address
        self.port = port
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket()
        self.sock.connect((self.address, self.port))
        # Authenticate

    def handshake(self, next_state: packet.State):
        if not self.sock:
            raise ValueError("I/O operation on closed connection.")

        handshake.HandshakePacket(
            protocol_version=340,
            server_address=self.address,
            server_port=self.port,
            next_state=next_state
        ).send(self.sock)

    def status(self, ping=True):
        if not self.sock:
            raise ValueError("I/O operation on closed connection.")
        if packet.state != packet.State.STATUS:
            raise ValueError(f"Can't request server status in {packet.state.name} state.")

        status.StatusRequestPacket().send(self.sock)
        server_status = packet.Packet.recv(self.sock).response

        if ping:
            payload = random.getrandbits(64)
            if payload > 0x8000000000000000:
                payload -= 0x10000000000000000

            t = time.time()
            status.PingPacket(payload=payload).send(self.sock)
            pong = packet.Packet.recv(self.sock)
            t = time.time() - t

            if pong.payload != payload:
                raise ValueError("Payload changed while pinging. The server might be compromised.")

            server_status['ping'] = t
        return server_status
