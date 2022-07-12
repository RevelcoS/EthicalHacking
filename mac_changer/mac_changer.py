#!usr/bin/env python

from optparse import OptionParser
import subprocess as cmd
import re

old = "00:0c:29:0c:03:8f"

def parse_args():
    parser = OptionParser()
    parser.add_option("-a", "--addr", type="string", dest="address", help="Specify a new MAC-address")
    parser.add_option("-i", "--interface", type="string", dest="target", help="Specify an interface")
    options = parser.parse_args()[0]
    if not options.target:
        parser.error("\n[-] Please, specify an interface")
    if not options.address:
        parser.error("\n[-] Please, specify a new MAC-address")
    return options


def get_current_address(target):
    output = str(cmd.check_output(["ifconfig", target]))
    address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
    if not address:
        print("[-] Bad interface")
        exit()
    else:
        return address.group(0)


def change_addr():
    options = parse_args()
    print("Current MAC-address = " + get_current_address(options.target))
    print("[+] Changing MAC-address to " + options.address + " for " + options.target)
    cmd.call(["ifconfig", options.target, "down"])
    cmd.call(["ifconfig", options.target, "hw", "ether", options.address])
    cmd.call(["ifconfig", options.target, "up"])

    address = get_current_address(options.target)
    if address == options.address:
        print("[+] MAC-address successfully changed")
    else:
        print("[-] Failed to change MAC-address: bad params")

change_addr()