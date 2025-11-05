import ipaddress
from textwrap import dedent
import random
import math

tools = [
    "   1. IP Address Conversion (Binary to Decimal)", 
    "   2. IP Address Conversion (Decimal to Binary)",
    "   3. IP Classification", 
    "   4. Subnet/CIDR Calculator", 
    "   5. Subnetting",
    "   6. VLSM",
]

red = "\033[31m"
cyan_underline = "\033[4;36m"
green_bold = "\033[1;32m"
bold = "\033[1m"
normal  = "\033[0m"

def logo():
    print("=" * 62)
    print(dedent(f"""\
 ____             _        _     _____                        
|  _ \ _   _  ___| | _____| |_  |_   _| __ __ _  ___ ___ _ __ 
| |_) | | | |/ __| |/ / _ \ __|   | || '__/ _` |/ __/ _ \ '__|
|  __/| |_| | (__|   <  __/ |_    | || | | (_| | (_|  __/ |   
|_|    \__, |\___|_|\_\___|\__|   |_||_|  \__,_|\___\___|_|   
       |___/                                                  """))
    print("=" * 62, "\n")

#########################
### Menus and Headers ###
#########################
def menu():
        print("\033c", end="")
        logo()
        global option
        print(*tools,sep="\n")
        print()
        print("=" * 62)
        print()
        while True:
            try:
                option = input("Select tool (Enter to exit): ")
                if option == "":
                    exit()
                else:
                    if int(option) >= 1 and int(option) <= 6:
                        tool(int(option))
                    else:
                        print(f"{red}Valid options: 1 to 6{normal}")
            except ValueError:
                print(f"{red}Valid options: 1 to 6{normal}")

def submenu():
    print(f"""\
    1. Main Menu
    0. Exit
    """)
    while True:
        try:
            sub_option = input("Select option (Enter to continue on current tool): ")
            if sub_option == "":
                tool(int(option))
            elif int(sub_option) == 1:
                menu()
            elif int(sub_option) == 0:
                exit()
            else:
                print(f"{red}Valid options: 0 or 1{normal}")
        except ValueError:
            print(f"{red}Valid options: 0 or 1{normal}")

def resultHeaderFooter():
    print()
    print("=" * 62, "\n")

def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 62}
        {green_bold}Pycket Tracer Tools{normal}
        {toolTitle[6:]}
        {"=" * 62}
        """))

######################
### Main Functions ###
######################
def tool(option):
    print("\033c", end="")
    if option == 1:
        decToBin()
    elif option == 2:
        binToDec()
    elif option == 3:
        ipClass()
    elif option == 4:
        subnetCIDR()
    elif option == 5:
        subnetting()
    elif option == 6:
        vlsm()

def decToBin():
    toolHeader()
    while True:
        try:
            decimalIP = input("Enter an IP Address (Decimal): ")
            if decimalIP == "":
                print()
                break
            else:
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                resultHeaderFooter()
                print(f"IP address (Binary): {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                resultHeaderFooter()
                break
        except ValueError:
            print(f"{red}Only valid IP Addresses allowed{normal} (Ex.: '{defaultDecimalIP()}')")
    submenu()

def binToDec():
    toolHeader()
    while True:
        try:
            binaryIP = input("Enter an IP address (Binary): ")
            if binaryIP == "":
                print()
                break
            else:
                binaryIP = binaryIP.replace(".", "")
                if len(binaryIP) == 32:
                    binaryIP = int(binaryIP, 2)
                    ip = ipaddress.IPv4Address(binaryIP)
                    resultHeaderFooter()
                    print(f"IP address (Decimal): {ip}")
                    resultHeaderFooter()
                    break
                else:
                    print(f"{red}Only valid IP addresses allowed{normal} (Ex.: '{defaultBinaryIP()}')")
        except ValueError:
            print(f"{red}Only valid IP addresses allowed{normal} (Ex.: '{defaultBinaryIP()}')")
    submenu()

def subnetCIDR():
    toolHeader()
    while True:
        try:
            hosts = input("Hosts required: ")
            if hosts == "":
                print()
                submenu()
            else:
                hosts = int(hosts)
                if hosts <= 4294967294:
                    break
                else:
                    print(f"{red}Number of possible hosts for IPv4 reached (4294967294), try a smaller network{normal}")
        except ValueError:
            print(f"{red}Enter integers only{normal}")
    totalHosts = hosts + 2
    bits = 0
    while (2 ** bits) < totalHosts:
        bits += 1
        cidr = 32 - bits
    while True:
        try:
            decimalIP = input("Enter the desired network IP: ")
            ip = ipaddress.IPv4Address(decimalIP)
            network = ipaddress.ip_network(f"{ip}/{cidr}")
            resultHeaderFooter()
            print(dedent(f"""\
                - Subnet Mask: {network.netmask}
                - CIDR: /{cidr}
                - Available IPs: {network.num_addresses - 2}
                - Network IP: {network.network_address}
                - First Usable IP: {ipaddress.IPv4Network(network)[1]}
                - Last Usable IP: {ipaddress.IPv4Network(network)[-2]}
                - Broadcast IP: {network.broadcast_address}
            """))
            resultHeaderFooter()
            break
        except (ValueError, UnboundLocalError):
            print(f"{red}Only valid network IP allowed{normal} (Ex:. 10.0.0.0)")
    submenu()

def ipClass():
    toolHeader()
    while True:
        try:
            ip = input("Enter an IP address (Decimal): ")
            if ip == "":
                print()
                break
            else:
                if ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('0.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('127.255.255.255'):
                    ip_class = str("Class A")
                elif ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('128.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('191.255.255.255'):
                    ip_class = str("Class B")
                elif ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('192.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('223.255.255.255'):
                    ip_class = str("Class C")
                if ipaddress.IPv4Address(ip).is_reserved is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is reserved (Class E)")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_link_local is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is link local")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_loopback is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is loopback")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_multicast is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is multicast (Class D)")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_private is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is private ({ip_class})")
                    resultHeaderFooter()
                    break
                else:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' is public ({ip_class})")
                    resultHeaderFooter()
                    break
        except ValueError:
            print(f"{red}Only valid IP addresses allowed{normal} (Ex.: '{defaultDecimalIP()}')")
    submenu()

def subnetting():
    toolHeader()
    while True:
        try:
            n_networks = input("Number of networks to configure: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 2:
                print(f"{red}Only integers greater than 1 allowed{normal}")
            else:
                break
        except ValueError:
            print(f"{red}Only integers greater than 1 allowed{normal}")
    while True:
        try:
            network_ip = input("Enter the desired initial network IP(CIDR): ")
            network = ipaddress.ip_network(network_ip)
            networks = {}
            n_networks = int(n_networks)
            bits_needed = math.ceil(math.log2(n_networks))
            new_prefix = network.prefixlen + bits_needed
            subnets = list(network.subnets(new_prefix=new_prefix))
            for netw in range(n_networks):
                networks[f'network_{netw}'] = {
                    'network_ip': subnets[netw],
                    'network_mask': subnets[netw].netmask,
                    'cidr': subnets[netw].prefixlen,
                    'hosts': subnets[netw].num_addresses-2,
                    'first_ip': subnets[netw][1],
                    'last_ip': subnets[netw][-2],
                    'broadcast_ip': subnets[netw].broadcast_address
                }
                netw += 1
            break
        except (ValueError, UnboundLocalError, IndexError):
            print(f"{red}Only valid network IP(CIDR) allowed (Ex:. 10.0.0.0/8){normal}")
    counter = 0
    print("=" * 62)
    while counter < n_networks: 
        print(dedent(f"""
            {cyan_underline}Network {counter+1}{normal}
            - CIDR: /{networks[list(networks)[counter]]['cidr']}
            - Subnet Mask: {networks[list(networks)[counter]]['network_mask']}
            - Network IP: {networks[list(networks)[counter]]['network_ip']}
            - First Usable IP: {networks[list(networks)[counter]]['first_ip']}
            - Last Usable IP: {networks[list(networks)[counter]]['last_ip']}
            - Broadcast IP: {networks[list(networks)[counter]]['broadcast_ip']}
            - Total Usable IPs: {networks[list(networks)[counter]]['hosts']}"""))
        counter += 1
    resultHeaderFooter()
    submenu()

def vlsm():
    toolHeader()
    while True:
        try:
            n_networks = input("Number of networks to configure: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 1:
                print(f"{red}Only positive integers allowed{normal}")
            else:
                break
        except ValueError:
            print(f"{red}Only positive integers allowed{normal}")
    networks = {}
    n_networks = int(n_networks)
    for netw in range(n_networks):
        while True:
            try:
                network_input = int(input(f"Hosts required for network {netw+1}: "))
                if network_input < 1:
                    print(f"{red}Only positive integers allowed{normal}")
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
                hosts_sum = sum(d['needed_hosts'] for d in networks.values() if d)
                if hosts_sum >= 4294967294:
                    print(f"{red}Number of possible hosts for IPv4 reached (4294967294), try a smaller network{normal}")
                else:
                    break
            except ValueError:
                print(f"{red}Only positive integers allowed{normal}")
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
            network0_ip = input("Enter the desired initial network IP: ")
            ip = ipaddress.IPv4Address(network0_ip)
            network0 = ipaddress.ip_network(f"{ip}/{sorted_networks[list(sorted_networks)[0]]['cidr']}")
            break
        except (ValueError, UnboundLocalError):
            print(f"{red}Only valid network IP allowed{normal} (Ex:. 10.0.0.0)")
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
    counter = -1
    print("=" * 62)
    while counter < n_networks - 1: 
        print(dedent(f"""
            {cyan_underline}Network {counter+2}{normal} ({networks[list(sorted_networks)[counter+1]]['needed_hosts']} hosts)
            - CIDR: /{networks[list(sorted_networks)[counter+1]]['cidr']}
            - Subnet Mask: {networks[list(sorted_networks)[counter+1]]['network_mask']}
            - Network IP: {networks[list(sorted_networks)[counter+1]]['network_ip']}
            - First Usable IP: {networks[list(sorted_networks)[counter+1]]['first_ip']}
            - Last Usable IP: {networks[list(sorted_networks)[counter+1]]['last_ip']}
            - Broadcast IP: {networks[list(sorted_networks)[counter+1]]['broadcast_ip']}
            - Total Usable IPs: {networks[list(sorted_networks)[counter+1]]['hosts']}
        """))
        counter += 1
    print("=" * 62, "\n")
    submenu()

#######################
### Other Functions ###
#######################
def defaultDecimalIP():
    randIP = []
    for x in range(4):
        randIP.append(str(random.randrange(0,256)))
    return ".".join(randIP)

def defaultBinaryIP():
    randIP = []
    for x in range(32):
        randIP.append(str(random.randrange(0,2)))
    randIP = "".join(randIP)
    return f"{randIP[0:9]}.{randIP[9:17]}.{randIP[17:25]}.{randIP[25:33]}"

menu()