from pymine.packets import packet
from pymine.types import Long, String


class StatusRequestPacket(packet.Packet):
    """A status request (state=1, id=0, serverbound) packet."""
    id = 0x00
    contents = {}


class StatusResponsePacket(packet.Packet):
    """A status response (state=1, id=0, clientbound) packet. Server response to StatusRequestPacket.
    response: server status, in JSON."""
    id = 0x00
    contents = {"response": String}


class PingPacket(packet.Packet):
    """A ping (state=1, id=1, serverbound) packet.
    payload: usually a random long."""
    id = 0x01
    contents = {"payload": Long}


class PongPacket(packet.Packet):
    """A pong (state=1, id=1, clientbound) packet. Server response to PingPacket.
    payload: should be the same as the one sent in the ping packet."""
    id = 0x01
    contents = {"payload": Long}


__packets__ = {
    0x00: StatusResponsePacket,
    0x01: PongPacket
}
