import json
import struct
import time
from io import BytesIO


# oh god no . . . wow, just use some mineflayer, I will happily provide help with it, this might take you a while

class RequestPacket:
    """A Python representation of a serverbound Minecraft Protocol packet."""

    def __init__(self, packet_id):
        self.payload = BytesIO()
        self.write_VarInt(packet_id)

    def write_boolean(self, value):
        """Writes a boolean into the packet."""
        self.write_byte(int(value))

    def write_byte(self, value):
        """Writes a byte into the packet."""
        self.payload.write(struct.pack('b', value))

    def write_unsigned_byte(self, value):
        """Writes an unsigned byte into the packet."""
        self.payload.write(struct.pack('B', value))

    def write_short(self, value):
        """Writes a short into the packet."""
        self.payload.write(struct.pack('h', value))

    def write_unsigned_short(self, value):
        """Writes an unsigned short into the packet."""
        self.payload.write(struct.pack('H', value))

    def write_int(self, value):
        """Writes an int into the packet."""
        self.payload.write(struct.pack('i', value))

    def write_long(self, value):
        """Writes a long into the packet."""
        self.payload.write(struct.pack('l', value))

    def write_float(self, value):
        """Writes a float into the packet."""
        self.payload.write(struct.pack('f', value))

    def write_double(self, value):
        """Writes a double into the packet."""
        self.payload.write(struct.pack('d', value))

    def write_String(self, n, value):
        """Writes a String (n) into the packet."""
        b = bytes(value[:n], 'utf8')
        self.write_VarInt(len(b))
        self.payload.write(b)

    @staticmethod
    def write_Var(stream, value):
        """Writes a Var-type into the stream."""
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                b |= 0x80
            stream.write(struct.pack('B', b))
            if not value:
                break

    def write_VarInt(self, value):
        """Writes a VarInt into the packet."""
        if value < 0:
            value += 0x100000000
        RequestPacket.write_Var(self.payload, value)

    def write_VarLong(self, value):
        """Writes a VarLong into the packet."""
        if value < 0:
            value += 0x10000000000000000
        RequestPacket.write_Var(self.payload, value)

    def write_byte_array(self, value):
        """Writes a byte array into the packet."""
        for v in value:
            if v < 0:
                v += 0x100
            self.payload.write(struct.pack('B', v))

    def send(self, socket):
        """Sends the packet."""
        b = self.payload.getvalue()
        length = BytesIO()
        RequestPacket.write_Var(length, len(b))
        socket.send(length.getvalue() + b)

    def send_compressed(self, socket):
        pass


class ResponsePacket:
    """A Python representation of a clientbound Minecraft Protocol packet."""

    def __init__(self, payload):
        self.payload = payload

    @staticmethod
    def recv(socket):
        """Receives a Packet from stream, identifies it and returns a Packet of the appropriate type."""
        print('Receiving packet')
        length = ResponsePacket.read_Var(socket.recv)
        print(f'  Packet length: {length}')
        packet_id = ResponsePacket.read_Var(socket.recv)
        print(f'  Packet ID: {packet_id}')
        # length -= math.ceil(packet_id.bit_length() / 7)
        time.sleep(5)
        payload = b''
        while len(payload) < length:
            # payload += socket.recv(length - len(payload))
            payload += socket.recv(1000000)
        print(f'  Payload: {payload}')
        if packet_id > length:
            packet_id, payload = ResponsePacket.uncompress(length, packet_id, payload)
        if packet_id not in packet_types:
            return ResponsePacket(BytesIO(payload)), packet_id
        return packet_types[state[0]][packet_id](BytesIO(payload))

    def read_boolean(self):
        """Reads a boolean from the packet."""
        return bool(self.read_byte())

    def read_byte(self):
        """Reads a byte from the packet."""
        return struct.unpack('b', self.payload.read(1))[0]

    def read_unsigned_byte(self):
        """Reads an unsigned byte from the packet."""
        return struct.unpack('B', self.payload.read(1))[0]

    def read_short(self):
        """Reads a short from the packet."""
        value = struct.unpack('h', self.payload.read(2))[0]
        return value

    def read_unsigned_short(self):
        """Reads a unsigned short from the packet."""
        value = struct.unpack('H', self.payload.read(2))[0]
        return value

    def read_int(self):
        """Reads an int from the packet."""
        return struct.unpack('i', self.payload.read(1))[0]

    def read_long(self):
        """Reads a long from the packet."""
        return struct.unpack('l', self.payload.read(1))[0]

    def read_float(self):
        """Reads a float from the packet."""
        return struct.unpack('f', self.payload.read(1))[0]

    def read_double(self):
        """Reads a double from the packet."""
        return struct.unpack('d', self.payload.read(1))[0]

    def read_String(self):
        """Reads a String from the packet."""
        print('  Reading String')
        length = self.read_VarInt()
        # print(f'    String length: {length}')
        # value = self.payload.read(length).decode('utf8')
        value = self.payload.read().decode('utf8')
        print(f'    String value: {value}')
        return value

    @staticmethod
    def read_Var(read):
        """Reads a Var-type from the stream."""
        value = 0
        while True:
            b = struct.unpack('B', read(1))[0]
            value = (value << 7) | (b & 0x7F)
            if not b & 0x80:
                return value

    def read_VarInt(self):
        """Reads a VarInt from the packet."""
        value = ResponsePacket.read_Var(self.payload.read)
        if value & 0x80000000:
            value -= 0x100000000
        return value

    def read_VarLong(self):
        """Reads a VarLong from the packet."""
        value = ResponsePacket.read_Var(self.payload.read)
        if value & 0x8000000000000000:
            value -= 0x10000000000000000
        return value

    def read_byte_array(self, length):
        """Reads a byte array from the packet."""
        value = []
        for i in range(length):
            value.append(self.read_byte())
        return value


class HandshakePacket(RequestPacket):
    def __init__(self, address, port, next_state):
        """state should be 1 for status or 2 for login."""
        if next_state not in (1, 2):
            raise ValueError(f"Possible states are 1 (status) and 2 (login) ({next_state} given)")
        state[0] = next_state
        super().__init__(0)
        self.write_VarInt(340)
        self.write_String(255, address)  # Server Address
        self.write_unsigned_short(port)  # Server Port
        self.write_VarInt(next_state)  # Next State


class StatusRequestPacket(RequestPacket):
    def __init__(self):
        if state[0] != 1:
            raise ValueError(f"Can't request server status in state {state[0]}")
        super().__init__(0)


class StatusResponsePacket(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.response = json.loads(self.read_String())

    def get_response(self):
        return self.response


class PingPacket(RequestPacket):
    def __init__(self, payload):
        super().__init__(1)
        self.write_long(payload)


class PongPacket(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.payload = self.read_long()

    def get_payload(self):
        return self.payload


class LoginStartPacket(RequestPacket):
    def __init__(self, username):
        super().__init__(0)
        self.write_String(16, username)


class LoginDisconnect(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.reason = json.loads(self.read_String())

    def get_reason(self):
        return self.reason


class EncryptionRequestPacket(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.server_id = self.read_String()
        self.pub_key = self.read_byte_array(self.read_VarInt())
        self.verify_token = self.read_byte_array(self.read_VarInt())

    def get_pub_key(self):
        return self.pub_key

    def get_verify_token(self):
        return self.verify_token


class EncryptionResponsePacket(RequestPacket):
    def __init__(self, shared_sec, verify_token):
        super().__init__(1)
        self.write_VarInt(len(shared_sec))
        self.write_byte_array(shared_sec)
        self.write_VarInt(len(verify_token))
        self.write_byte_array(verify_token)


class LoginSuccessPacket(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.uuid = self.read_String()
        self.username = self.read_String()
        state[0] = 3

    def get_uuid(self):
        return self.uuid

    def get_username(self):
        return self.username


class SetCompressionPacket(ResponsePacket):
    def __init__(self, payload):
        super().__init__(payload)
        self.threshold = self.read_VarInt()

    def get_threshold(self):
        return self.threshold


state = [0]  # 0 for handshake, 1 for status, 2 for login and 3 for play

packet_types = {
    0: {},
    1: {
        0: StatusResponsePacket,
        1: PongPacket
    },
    2: {
        0: LoginDisconnect,
        1: EncryptionRequestPacket,
        2: LoginStartPacket
    }
}
