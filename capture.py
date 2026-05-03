from scapy.all import sniff
from utils import extract_features

def start_capture():
    data = []

    def process(packet):
        features = extract_features(packet)
        data.append(features)

    sniff(prn=process, count=20)
    return data