from pymine import packet
from pymine.types import Long, String


class StatusRequestPacket(packet.Packet):
    id = 0x00
    contents = {}


class StatusResponsePacket(packet.Packet):
    id = 0x00
    contents = {"response": String}


class PingPacket(packet.Packet):
    id = 0x01
    contents = {"payload": Long}


class PongPacket(packet.Packet):
    id = 0x01
    contents = {"payload": Long}


__packets__ = {
    0x00: StatusResponsePacket,
    0x01: PongPacket
}
