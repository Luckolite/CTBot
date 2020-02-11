from pymine import types
from pymine.packets import packet


class LoginStartPacket(packet.Packet):
    """A login start (state=2, id=0, serverbound) packet.
    username: the username of the player."""

    id = 0x00
    contents = {"username": types.String}


class DisconnectPacket(packet.Packet):
    """A disconnect (state=2, id=0, clientbound) packet.
    reason: the reason for disconnecting."""

    id = 0x00
    contents = {"reason": types.String}


class EncryptionRequestPacket(packet.Packet):
    """An encryption request (state=2, id=1, clientbound) packet.
    server_id: usually an empty string.
    public_key: servers public key for sending the shared secret.
    verify_token: the token for verifying encryption."""

    id = 0x01
    contents = {
        "server_id": types.String,
        "public_key": types.ByteArray,
        "verify_token": types.ByteArray,
    }


class EncryptionResponsePacket(packet.Packet):
    """An encryption response (state=2, id=1, serverbound) packet. Client response to EncryptionRequestPacket.
    shared_secret: the client-generated secret, encrypted with the server's public key.
    verify_token: verify_token, encrypted with the server's public key, for verifying encryption."""

    id = 0x01
    contents = {"shared_secret": types.ByteArray, "verify_token": types.ByteArray}


class LoginSuccessPacket(packet.Packet):
    """A login success (state=2, id=2, clientbound) packet.
    Switches state to 3 (play)."""

    id = 0x02
    contents = {"uuid": types.String, "username": types.String}


class SetCompressionPacket(packet.Packet):
    """A set compression (state=2, id=3, clientbound) packet.
    Sets compression threshold to threshold.
    threshold: the new compression threshold."""

    id = 0x03
    contents = {"threshold": types.VarInt}


__packets__ = {
    0x00: DisconnectPacket,
    0x01: EncryptionRequestPacket,
    0x02: LoginSuccessPacket,
    0x03: SetCompressionPacket,
}
