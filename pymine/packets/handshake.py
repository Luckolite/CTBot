from pymine.packets import packet
from pymine.types import VarInt, String, UnsignedShort


class HandshakePacket(packet.Packet):
    """A handshake (state=0, id=0, serverbound) packet.
    Switches state to next_state.
    protocol_version: the version of the protocol to use, currently only 340 is supported.
    server_address: the address of the server this is sent to. The Notchian server does not use this information.
    server_port: the port of the server this is sent to. The Notchian server does not use this information.
    next_state: the state of the connection to switch to (1 for status, 2 for login)."""
    id = 0x00
    contents = {
        "protocol_version": VarInt,
        "server_address": String,
        "server_port": UnsignedShort,
        "next_state": VarInt,
    }


__packets__ = {}
