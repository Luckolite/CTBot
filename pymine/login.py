from pymine import packet, types


class LoginStart(packet.Packet):
    id = 0x00
    contents = {
        'username': types.String
    }


class Disconnect(packet.Packet):
    id = 0x00
    contents = {
        'reason': types.String
    }


class EncryptionRequest(packet.Packet):
    id = 0x01
    contents = {
        'server_id': types.String,
        'public_key_length': types.VarInt,
        'public_key': types.ByteArray,
        'verify_token_length': types.VarInt,
        'verify_token': types.ByteArray
    }


class EncryptionResponse(packet.Packet):
    id = 0x01
    contents = {
        'shared_secret_length': types.VarInt,
        'shared_secret': types.ByteArray,
        'verify_token_length': types.VarInt,
        'verify_token': types.ByteArray
    }


class LoginSuccessPacket(packet.Packet):
    id = 0x02
    contents = {
        'uuid': types.String,
        'username': types.String
    }


class SetCompressionPacket(packet.Packet):
    id = 0x03
    contents = {
        'threshold': types.VarInt
    }


__packets__ = {
    0x00: Disconnect,
    0x01: EncryptionRequest,
    0x02: LoginSuccessPacket,
    0x03: SetCompressionPacket
}
