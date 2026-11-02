"""Bounded length-prefixed byte format used only by the local worked lab."""
def encode(payload):
    if not isinstance(payload,bytes) or len(payload)>64:
        raise ValueError('payload must be <=64 bytes')
    return bytes([len(payload)])+payload

def decode(packet):
    if not isinstance(packet,bytes) or not packet or packet[0]>64 or len(packet)!=packet[0]+1:
        raise ValueError('invalid frame')
    return packet[1:]
