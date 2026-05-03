from scapy.all import *

def extract_features(packet):
    length = len(packet)

    if packet.haslayer(TCP):
        protocol = 1
        port = packet.sport
    elif packet.haslayer(UDP):
        protocol = 2
        port = packet.sport
    else:
        protocol = 0
        port = 0

    return [length, protocol, port]