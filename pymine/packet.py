from types import VarInt


class Packet:
    id = None
    contents = None

    def __init__(self, **kwargs):
        self.data = {}
        for k in self.self.contents:
            self.data[k] = None
        for key, value in kwargs.items():
            if key not in self.contents:
                raise NameError(f"{type(self).__name__} has no field '{key}'")
            if not isinstance(value, self.contents[key]):
                raise TypeError(f"{key} field must be '{self.contents[key].__name__}', not '{type(value).__name__}'")
            self.data[key] = value

    def __getattr__(self, item):
        if item not in self.self.contents:
            raise NameError(f"{type(self).__name__} has no field '{item}'")
        return self.data[item]

    def __setattr__(self, key, value):
        if key not in self.contents:
            raise NameError(f"{type(self).__name__} has no field '{key}'")
        if not isinstance(value, self.contents[key]):
            raise TypeError(f"{key} field must be '{self.contents[key].__name__}', not '{type(value).__name__}'")
        self.__dict__['data'][key] = value

    def send(self, socket):
        buf = bytearray()
        buf.append(VarInt(self.id).pack())
        for key, value in self.data.items():
            if value is None:
                raise ValueError(f'{key} field is blank')
            if hasattr(value, 'pack'):
                buf.append(value.pack())
        socket.send(VarInt(len(buf)).pack())
        socket.send(buf)
