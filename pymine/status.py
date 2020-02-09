from pymine import packet
from pymine.types import Long, String


class StatusRequestPacket(packet.Packet):
    id = 0
    contents = {}


class StatusResponsePacket(packet.Packet):
    id = 0
    contents = {"response": String}


class PingPacket(packet.Packet):
    id = 1
    contents = {"payload": Long}


class PongPacket(packet.Packet):
    id = 1
    contents = {"payload": Long}


__packets__ = {0: StatusResponsePacket, 1: PongPacket}
