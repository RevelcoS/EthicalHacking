from re import subn
import scapy.all as scapy
from argparse import ArgumentParser
import subprocess, re

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="Specify receiver's IP")
    return parser.parse_args()


def parse(answered_list):
    parsed_answered_list = []
    for answer in answered_list:
        parsed_answered_list.append({"ip":answer[1].psrc, "mac":answer[1].hwsrc})
    return parsed_answered_list


def get_ip_range():
    return re.search(
        r"\d?\d?\d?\.\d?\d?\d?\.\d?\d?\d?\.\d?\d?\d?",
        str(subprocess.check_output(["ifconfig", "eth0"]))
    ).group(0) + "/24"


def scan(ip):
    ip = ip or get_ip_range()
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_arp_req = broadcast/arp_req
    answered_list = scapy.srp(broadcast_arp_req, timeout=1, verbose=False)[0]
    return parse(answered_list)


def output(parsed_answered_list):
    print("IP", "MAC", sep="\t"*3)
    for answer in parsed_answered_list:
        print(answer["ip"], answer["mac"], sep="\t"*2)

if __name__ == "__main__":
    output(scan(parse_args().ip))