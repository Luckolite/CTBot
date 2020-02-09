<<<<<<< HEAD
class VarInt:
    def __init__(self, n):
        if not -0x80000000 < n < 0x7FFFFFFF:
            raise ValueError(
                "VarInt can only store numbers between -2147483648 and 2147483647"
            )
        self.n = n
=======
# import json
import struct
from abc import ABC, abstractmethod
>>>>>>> 0a074bf9f090b1e053a5c1bd75697fac7fbbdf28


class Type(ABC):
    @staticmethod
    @abstractmethod
    def pack(value):
        pass

    @staticmethod
    @abstractmethod
    def unpack(read):
        pass


class Boolean(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, bool):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Boolean")
        return struct.pack('b', value)

    @staticmethod
    def unpack(read):
        return bool(struct.unpack('b', read(1))[0])


class Byte(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Byte")
        if not -0x80 <= value <= 0x7F:
            raise ValueError('Byte can only store values between -128 and 127')
        return struct.pack('b', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('b', read(1))[0]


class UnsignedByte(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to UnsignedByte")
        if not 0 <= value <= 0xFF:
            raise ValueError('UnsignedByte can only store values between 0 and 255')
        return struct.pack('B', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('B', read(1))[0]


class Short(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Short")
        if not -0x8000 <= value <= 0x7FFF:
            raise ValueError('Short can only store values between -32768 and 32767')
        return struct.pack('h', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('h', read(2))[0]


class UnsignedShort(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to UnsignedShort")
        if not 0 <= value <= 0xFFFF:
            raise ValueError('UnsignedShort can only store values between 0 and 65535')
        return struct.pack('H', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('H', read(2))[0]


class Int(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Int")
        if not -0x80000000 <= value <= 0x7FFFFFFF:
            raise ValueError('Int can only store values between -2147483648 and 2147483647')
        return struct.pack('i', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('i', read(4))[0]


class Long(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Long")
        if not -0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF:
            raise ValueError('Long can only store values between -9223372036854775808 and 9223372036854775807')
        return struct.pack('l', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('l', read(8))[0]


class Float(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, float):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Float")
        return struct.pack('f', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('f', read(4))[0]


class Double(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, float):
            raise TypeError(f"'{type(value).__name__}' can't be converted to Double")
        return struct.pack('d', value)

    @staticmethod
    def unpack(read):
        return struct.unpack('d', read(8))[0]


class String(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, str):
            raise TypeError(f"'{type(value).__name__}' can't be converted to String")
        data = bytes(value, 'utf8')
        return VarInt.pack(len(data)) + data

    @staticmethod
    def unpack(read):
        length = VarInt.unpack(read)
        data = bytearray()
        while len(data) < length:
            data.extend(read(length))
        string = data.decode('utf8')
        return string


class VarInt(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to VarInt")
        if not -0x80000000 <= value <= 0x7FFFFFFF:
            raise ValueError('VarInt can only store values between -2147483648 and 2147483647')
        data = bytearray()
        value = value
        if value < 0:
            value += 0x100000000
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                data.append(b | 0x80)
            else:
                data.append(b)
                return data

    @staticmethod
    def unpack(read):
        value = 0
        while True:
            b = struct.unpack('B', read(1))[0]
            value = value << 7 | b & 0x7F
            if not b & 0x80:
                if value & 0x80000000:
                    value -= 0x100000000
                return value


class VarLong(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(f"'{type(value).__name__}' can't be converted to VarInt")
        if not -0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF:
            raise ValueError('VarLong can only store values between -9223372036854775808 and 9223372036854775807')
        data = bytearray()
        value = value
        if value < 0:
            value += 0x10000000000000000
        while True:
            b = value & 0x7F
            if value:
                data.append(b | 0x80)
                value >>= 7
            else:
                data.append(b)
                return data

    @staticmethod
    def unpack(read):
        value = 0
        while True:
            b = read(1)
            value = value << 7 | b & 0x7F
            if not b & 0x80:
                if value & 0x8000000000000000:
                    value -= 0x10000000000000000
                return value
