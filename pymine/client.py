import json
import random
import socket
import time

from pymine.packets import packet, handshake, status, login


class LoginError(ConnectionError):
    pass


class Client:
    def __init__(
        self, address, port=25565, target_state: packet.State = packet.State.STATUS
    ):
        if target_state not in (packet.State.STATUS, packet.State.LOGIN):
            raise ValueError(
                f"Target state should be STATUS or LOGIN, not '{target_state.name}'"
            )

        self.address = address
        self.port = port

        self.sock = None

        self.target_state = target_state

        self.uuid = None
        self.username = None

    def __enter__(self):
        self.open()
        return self

    def open(self):
        """Opens a connection to the server, performing a handshake and switching to the target state."""
        if self.sock:
            raise ValueError("already open")

        self.sock = socket.socket()
        self.sock.connect((self.address, self.port))
        if self.target_state == packet.State.LOGIN:
            pass  # Authenticate

        handshake.HandshakePacket(
            protocol_version=340,
            server_address=self.address,
            server_port=self.port,
            next_state=self.target_state.value,
        ).send(self.sock)

        packet.state = self.target_state

    def status(self, ping=True):
        """Requests server status and pings the server (if ping is set)."""
        if not self.sock:
            raise ValueError("I/O operation on closed connection.")
        if packet.state != packet.State.STATUS:
            raise ValueError(
                f"Can't request server status in '{packet.state.name}' state."
            )

        status.StatusRequestPacket().send(self.sock)
        server_status = json.loads(packet.Packet.recv(self.sock).response)

        if ping:
            payload = random.getrandbits(64)
            if payload > 0x8000000000000000:
                payload -= 0x10000000000000000

            t = time.time()
            status.PingPacket(payload=payload).send(self.sock)
            pong = packet.Packet.recv(self.sock)
            server_status["ping"] = (time.time() - t) * 1000

            if pong.payload != payload:
                raise ValueError(
                    "Payload changed while pinging. The server might be compromised."
                )

        self.close()

        return server_status

    def login(self, username):
        if not self.sock:
            raise ValueError("I/O operation on closed connection.")
        if packet.state != packet.State.LOGIN:
            raise ValueError(
                f"Can't request server status in {packet.state.name} state."
            )

        login.LoginStartPacket(username=username).send(self.sock)

        while True:
            next_packet = packet.Packet.recv(self.sock)
            if next_packet.id == 0x00:
                raise LoginError(next_packet.reason)
            elif next_packet.id == 0x01:
                # Auth
                login.EncryptionResponsePacket().send(self.sock)
            elif next_packet.id == 0x02:
                self.uuid = next_packet.uuid
                self.username = next_packet.username
            elif next_packet.id == 0x03:
                packet.compressionThreshold = next_packet.threshold

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes this client, freeing the resources and de-authenticating."""
        if self.sock:
            self.sock.close()
            self.sock = None
