from pymine import packet
from pymine.types import VarInt, String, UnsignedShort


class HandshakePacket(packet.Packet):
    id = 0x00
    contents = {
        "protocol_version": VarInt,
        "server_address": String,
        "server_port": UnsignedShort,
        "next_state": VarInt,
    }

    def send(self, socket):
        super().send(socket)
        packet.state = int(self.next_state)


__packets__ = {}
