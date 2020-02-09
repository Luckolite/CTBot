from io import BytesIO
from typing import Dict, Type

from pymine import types

state = 0


def reset():
    global state
    state = 0


class Packet:
    id: int = None
    contents: Dict[str, Type[types.Type]] = None

    def __init__(self, stream=None, **kwargs):
        if self.id is None or self.contents is None:
            raise ValueError("Invalid packet signature or Packet creation attempt")
        self.__dict__['data'] = {}

        for k in self.contents:
            self.data[k] = None

        if stream:
            if not hasattr(stream, 'read'):
                raise TypeError(f"stream should be a byte stream, not '{type(stream).__name__}'")
            for key, value in self.contents.items():
                self.__setattr__(key, value.unpack(stream.read))

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __getattr__(self, item):
        if item not in self.contents:
            raise NameError(f"{type(self).__name__} has no field '{item}'")
        return self.data[item]

    def __setattr__(self, key, value):
        if key not in self.contents:
            raise NameError(f"{type(self).__name__} has no field '{key}'")
        self.__dict__['data'][key] = value

    @staticmethod
    def recv(socket):
        if state == 0:
            from pymine.handshake import __packets__
        elif state == 1:
            from pymine.status import __packets__
        elif state == 2:
            from pymine.login import __packets__
        elif state == 3:
            from pymine.play import __packets__
        else:
            raise ValueError(f"Illegal state: {state}")

        packet_len = int(types.VarInt.unpack(socket.recv))
        data = BytesIO()
        while data.tell() < packet_len:
            data.write(socket.recv(packet_len))
        data.seek(0)
        packet_id = int(types.VarInt.unpack(data.read))
        return __packets__[packet_id](data)

    def send(self, socket):
        buf = bytearray()
        buf.extend(types.VarInt.pack(self.id))
        for key, value in self.data.items():
            if value is None:
<<<<<<< HEAD
                raise ValueError(f"{key} field is blank")
            if hasattr(value, "pack"):
                buf.append(value.pack())
        socket.send(VarInt(len(buf)).pack())
=======
                raise ValueError(f'{key} field is blank')
            buf.extend(self.contents[key].pack(value))
        socket.send(types.VarInt.pack(len(buf)))
>>>>>>> 0a074bf9f090b1e053a5c1bd75697fac7fbbdf28
        socket.send(buf)
