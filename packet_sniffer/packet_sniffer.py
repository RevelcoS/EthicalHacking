import scapy.all as scapy
from scapy.layers import http
import codecs

def sniff(interafce):
    scapy.sniff(iface=interafce, store=False, prn=parse_packet)

def parse_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet[http.HTTPRequest].show())
        """ if packet.haslayer(scapy.Raw):
            res = str(packet[scapy.Raw].load)
            print(res, end="\n\n") """

if __name__ == "__main__":
    sniff("eth0")