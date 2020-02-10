# import json
import struct
from abc import ABC, abstractmethod


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
            raise TypeError(
                f"Byte.pack() argument must be a bool, not '{type(value).__name__}'"
            )
        return struct.pack("b", value)

    @staticmethod
    def unpack(read):
        return bool(struct.unpack("b", read(1))[0])


class Byte(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"Byte.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x80 <= value <= 0x7F:
            raise ValueError(f"Byte.pack() requires -128 <= number <= 127")
        return struct.pack("b", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("b", read(1))[0]


class UnsignedByte(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"UnsignedByte.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not 0 <= value <= 0xFF:
            raise ValueError(f"UnsignedByte.pack() requires 0 <= number <= 255")
        return struct.pack("B", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("B", read(1))[0]


class Short(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"Short.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x8000 <= value <= 0x7FFF:
            raise ValueError(f"Short.pack() requires -32768 <= number <= 32767")
        return struct.pack("h", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("h", read(2))[0]


class UnsignedShort(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"UnsignedShort.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not 0 <= value <= 0xFFFF:
            raise ValueError(f"UnsignedShort.pack() requires 0 <= number <= 65535")
        return struct.pack("H", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("H", read(2))[0]


class Int(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"Int.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x80000000 <= value <= 0x7FFFFFFF:
            raise ValueError(f"Int.pack() requires -2147483648 <= number <= 2147483647")
        return struct.pack("i", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("i", read(4))[0]


class Long(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"Long.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF:
            raise ValueError(
                f"Long.pack() requires -9223372036854775808 <= number <= 9223372036854775807"
            )
        return struct.pack("l", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("l", read(8))[0]


class Float(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, float):
            raise TypeError(
                f"Float.pack() argument must be a float, not '{type(value).__name__}'"
            )
        return struct.pack("f", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("f", read(4))[0]


class Double(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, float):
            raise TypeError(
                f"Double.pack() argument must be a float, not '{type(value).__name__}'"
            )
        return struct.pack("d", value)

    @staticmethod
    def unpack(read):
        return struct.unpack("d", read(8))[0]


class String(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, str):
            raise TypeError(
                f"String.pack() argument must be a str, not '{type(value).__name__}'"
            )
        data = bytes(value, "utf8")
        return VarInt.pack(len(data)) + data

    @staticmethod
    def unpack(read):
        length = VarInt.unpack(read)
        data = bytearray()
        while len(data) < length:
            data.extend(read(length))
        string = data.decode("utf8")
        return string


class VarInt(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"VarInt.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x80000000 <= value <= 0x7FFFFFFF:
            raise ValueError(
                f"VarInt.pack() requires -2147483648 <= number <= 2147483647"
            )
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
        i = 0
        while True:
            b = struct.unpack("B", read(1))[0]
            value |= (b & 0x7F) << (i * 7)
            i += 1
            if not b & 0x80:
                if value & 0x80000000:
                    value -= 0x100000000
                return value


class VarLong(Type):
    @staticmethod
    def pack(value):
        if not isinstance(value, int):
            raise TypeError(
                f"VarLong.pack() argument must be an int, not '{type(value).__name__}'"
            )
        if not -0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF:
            raise ValueError(
                f"VarLong.pack() requires -9223372036854775808 <= number <= 9223372036854775807"
            )
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


class ByteArray(Type):
    @staticmethod
    def pack(values):
        if not hasattr(values, "__iter__"):
            raise TypeError(f"'{type(values).__name__}' object is not iterable")
        return struct.pack(f"{len(values)}B", *values)

    @staticmethod
    def unpack(read):
        size = VarInt.unpack(read)
        return struct.unpack(f"{size}B", read(size))
