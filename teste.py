import ipaddress
import random
from textwrap import dedent
import hashlib
import getpass
import string
import pprint
 
def vlsm():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 50}
        VLSM
        {"=" * 50}"""))
    while True:
        try:
            n_networks = int(input("Number of Networks to Configure: "))
            if n_networks < 1:
                print("Only positive integers allowed")
            else:
                break
        except ValueError:
            print("Only positive integers allowed")
    networks = {}
    for netw in range(n_networks):
        while True:
            try:
                network_input = int(input(f"Enter the number of hosts for Network {netw+1}: "))
                if network_input < 1:
                    print("Only positive integers allowed")
                else:
                    networks[f'network_{netw}'] = {
                        'needed_hosts': network_input,
                        'needed_ips': network_input + 2,
                        'network_mask': None,
                        'cidr': None,
                        'hosts': None,
                        'network_ip': None,
                        'first_ip': None,
                        'last_ip': None,
                        'broadcast_ip': None
                    }
                    break
            except ValueError:
               print("Only positive integers allowed")
    counter = 0
    while counter < n_networks:
        cidr = 0
        bits = 0
        totalHosts = networks[f'network_{counter}']['needed_ips']
        while (2 ** bits) < totalHosts:
            bits += 1
            cidr = (32 - bits)
        networks[f'network_{counter}']['cidr'] = cidr
        counter += 1
    sorted_networks = dict(sorted(networks.items(), reverse=True, key=lambda item: item[1]['needed_hosts']))
    while True:
        try:
            network0_ip = input("Insert the initial Network IP: ")
            ip = ipaddress.IPv4Address(network0_ip)
            network0 = ipaddress.ip_network(f"{ip}/{sorted_networks[list(sorted_networks)[0]]['cidr']}")
            break
        except (ValueError, UnboundLocalError):
            print("Try again")
    networks[list(sorted_networks)[0]]['network_mask'] = network0.netmask
    networks[list(sorted_networks)[0]]['hosts'] = (network0.num_addresses - 2)
    networks[list(sorted_networks)[0]]['network_ip'] = network0.network_address
    networks[list(sorted_networks)[0]]['first_ip'] = network0[1]
    networks[list(sorted_networks)[0]]['last_ip'] = network0[-2]
    networks[list(sorted_networks)[0]]['broadcast_ip'] = network0.broadcast_address
    for x in range(n_networks - 1):
        network_ip = (sorted_networks[list(sorted_networks)[x]]['broadcast_ip'])+1
        network_n = ipaddress.ip_network(f"{network_ip}/{sorted_networks[list(sorted_networks)[x+1]]['cidr']}")
        networks[list(sorted_networks)[x+1]]['network_mask'] = network_n.netmask
        networks[list(sorted_networks)[x+1]]['hosts'] = (network_n.num_addresses - 2)
        networks[list(sorted_networks)[x+1]]['network_ip'] = network_n.network_address
        networks[list(sorted_networks)[x+1]]['first_ip'] = network_n[1]
        networks[list(sorted_networks)[x+1]]['last_ip'] = network_n[-2]
        networks[list(sorted_networks)[x+1]]['broadcast_ip'] = network_n.broadcast_address
    sorted_networks = dict(sorted(networks.items(), reverse=True, key=lambda item: item[1]['needed_hosts']))
    y -= 1
    for y in range(n_networks):  
        print(dedent(f"""
            Network {y+2}
            CIDR: /{networks[list(sorted_networks)[y+1]]['cidr']}
            Subnet Mask: {networks[list(sorted_networks)[y+1]]['network_mask']}
            Network IP: {networks[list(sorted_networks)[y+1]]['network_ip']}
            First Usable IP: {networks[list(sorted_networks)[y+1]]['first_ip']}
            Last Usable IP: {networks[list(sorted_networks)[y+1]]['last_ip']}
            Broadcast IP: {networks[list(sorted_networks)[y+1]]['broadcast_ip']}
        """))

vlsm()

