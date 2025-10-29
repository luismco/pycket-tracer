import ipaddress
import random
from textwrap import dedent
import hashlib
import getpass
import string
 
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
    for x in range(n_networks):
        while True:
            try:
                network_input = int(input(f"Enter the number of hosts for Network {x+1}: "))
                if network_input < 1:
                    print("Only positive integers allowed")
                else:
                    networks[f'network_{x}'] = {
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
        except ValueError:
            print("Try again")
    networks[list(sorted_networks)[0]]['network_mask'] = network0.netmask
    networks[list(sorted_networks)[0]]['hosts'] = (network0.num_addresses - 2)
    networks[list(sorted_networks)[0]]['network_ip'] = network0.network_address
    networks[list(sorted_networks)[0]]['first_ip'] = network0[1]
    networks[list(sorted_networks)[0]]['last_ip'] = network0[-2]
    networks[list(sorted_networks)[0]]['broadcast_ip'] = network0.broadcast_address
    print(networks)


    



vlsm()

