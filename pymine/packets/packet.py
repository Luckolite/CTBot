import enum
import socket
import zlib
from io import BytesIO
from typing import Dict, Type

from pymine import types


class State(enum.Enum):
    """A connection state enum."""

    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


state = State.HANDSHAKE
compressionThreshold = -1


class Packet:
    """A base class for all packets. id and contents should be redefined in subclasses."""

    id: int = None
    contents: Dict[str, Type[types.Type]] = None

    def __init__(self, stream=None, **kwargs):
        if (
                self.id is None or self.contents is None
        ):  # Should be redefined in subclasses
            raise ValueError("Invalid packet signature or Packet creation attempt")
        self.__dict__["data"] = {}  # Initialize data

        for k in self.contents:  # Initialize fields
            self.data[k] = None

        if stream:  # Read fields from stream
            if not hasattr(stream, "read"):
                raise TypeError(
                    f"stream should be a byte stream, not '{type(stream).__name__}'"
                )
            for key, value in self.contents.items():
                self.__setattr__(key, value.unpack(stream.read))

        for key, value in kwargs.items():  # Read fields from kwargs
            self.__setattr__(key, value)

    def __getattr__(self, item):
        if item not in self.contents:  # Field should exist
            raise NameError(f"{type(self).__name__} has no field '{item}'")
        return self.data[item]

    def __setattr__(self, key, value):
        if key not in self.contents:  # Field should exist
            raise NameError(f"{type(self).__name__} has no field '{key}'")
        self.__dict__["data"][key] = value

    @staticmethod
    def recv(sock: socket.socket):
        """Receives a Packet from stream."""
        if state == State.HANDSHAKE:
            from pymine.packets.handshake import __packets__
        elif state == State.STATUS:
            from pymine.packets.status import __packets__
        elif state == State.LOGIN:
            from pymine.packets.login import __packets__
        elif state == State.PLAY:
            from pymine.packets.play import __packets__
        else:
            raise ValueError(f"Illegal state: {state}")

        packet_len = int(types.VarInt.unpack(sock.recv))
        data = BytesIO()
        while data.tell() < packet_len:
            data.write(sock.recv(packet_len))
        data.seek(0)
        if compressionThreshold >= 0:
            data_len = types.VarInt.unpack(data.read)
            if data_len != 0:  # Compression is enabled and the packet is compressed
                if (
                        data_len < compressionThreshold
                ):  # Uncompressed length should be over the threshold
                    raise ProtocolError(
                        "packets should be compressed only if length over the threshold, the server may be compromised"
                    )
                data = BytesIO(zlib.decompress(data.read()))
        packet_id = int(types.VarInt.unpack(data.read))
        return __packets__[packet_id](data)

    def send(self, sock: socket.socket):
        """Sends the packet to stream."""
        buf = bytearray()
        buf.extend(types.VarInt.pack(self.id))  # Write Packet ID and fields
        for key, value in self.data.items():
            if value is None:  # All fields should be filled
                raise ValueError(f"{key} field is blank")
            buf.extend(self.contents[key].pack(value))
        if compressionThreshold >= 0:
            if (
                    len(buf) > compressionThreshold
            ):  # Compression is enabled and the amount of data is over the threshold
                buf = types.VarInt.pack(len(buf)) + zlib.compress(buf)
            else:  # Compression is enabled, but can send without compression
                buf = types.VarInt.pack(0) + buf
        sock.send(
            types.VarInt.pack(len(buf))
        )  # Send packet length and the packet itself
        sock.send(buf)


class ProtocolError(IOError):
    pass
