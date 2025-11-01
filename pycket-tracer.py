import ipaddress
from textwrap import dedent
import random
import math

tools = [
    "1. IP Address Conversion (Binary to Decimal)", 
    "2. IP Address Conversion (Decimal to Binary)",
    "3. IP Classification", 
    "4. Subnet Calculator", 
    "5. Subnetting",
    "6. VLSM",
]

#########################
### Menus and Headers ###
#########################
def menu():
        print("\033c", end="")
        global option
        print(dedent(f"""
            {"=" * 80}
            Pycket Tracer Tools
            {"=" * 80}"""))
        print(*tools,sep="\n")
        while True:
            try:
                option = input("\nSelect tool (Enter to exit): ")
                if option == "":
                    exit()
                else:
                    if int(option) >= 1 and int(option) <= 6:
                        tool(int(option))
                    else:
                        print("Valid options: 1 to 6")
            except ValueError:
                print("Valid options: 1 to 6")

def submenu():
    print(dedent(f"""\
        1. Main Menu
        0. Exit    
        """))
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
                print("Valid options: 0 or 1")
        except ValueError:
            print("Valid options: 0 or 1")

def resultHeader():
    print(dedent(f"""
        {"=" * 80}
        *** Result ***"""))

def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 80}
        Pycket Tracer Tools
        {toolTitle[3:]}
        {"=" * 80}
        """))

######################
### Main Functions ###
######################
def tool(option):
    print("\033c", end="")
    if option == 1:
        toolHeader()
        while True:
            try:
                decimalIP = input("Enter an IP Address (Decimal): ")
                if decimalIP == "":
                    print()
                    break
                else:
                    ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                    resultHeader()
                    print(f"IP address (Binary): {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                    print("=" * 80, "\n")
                    break
            except ValueError:
                print(f"Only valid IP Addresses allowed (Ex.: '{defaultDecimalIP()}')")
        submenu()
    elif option == 2:
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
                        resultHeader()
                        print(f"IP address (Decimal): {ip}")
                        print("=" * 80, "\n")
                        break
                    else:
                        print(f"Only valid IP addresses allowed (Ex.: '{defaultBinaryIP()}')")
            except ValueError:
                print(f"Only valid IP addresses allowed (Ex.: '{defaultBinaryIP()}')")
        submenu()
    elif option == 3:
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
                        resultHeader()
                        print(f"The IP '{ip}' is reserved (Class E)")
                        print("=" * 80, "\n")
                        break
                    elif ipaddress.IPv4Address(ip).is_link_local is True:
                        resultHeader()
                        print(f"The IP '{ip}' is link local")
                        print("=" * 80, "\n")
                        break
                    elif ipaddress.IPv4Address(ip).is_loopback is True:
                        resultHeader()
                        print(f"The IP '{ip}' is loopback")
                        print("=" * 80, "\n")
                        break
                    elif ipaddress.IPv4Address(ip).is_multicast is True:
                        resultHeader()
                        print(f"The IP '{ip}' is multicast (Class D)")
                        print("=" * 80, "\n")
                        break
                    elif ipaddress.IPv4Address(ip).is_private is True:
                        resultHeader()
                        print(f"The IP '{ip}' is private ({ip_class})")
                        print("=" * 80, "\n")
                        break
                    else:
                        resultHeader()
                        print(f"The IP '{ip}' is public ({ip_class})")
                        print("=" * 80, "\n")
                        break
            except ValueError:
                print(f"Only valid IP addresses allowed (Ex.: '{defaultDecimalIP()}')")
        submenu()
    elif option == 4:
        toolHeader()
        while True:
            try:
                hosts = input("Hosts required: ")
                if hosts == "":
                    print()
                    submenu()
                else:
                    hosts = int(hosts)
                    break
            except ValueError:
                print("Enter integers only")
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
                print()
                print("=" * 80)
                print(dedent(f"""
                    - Subnet Mask: {network.netmask}
                    - CIDR: /{cidr}
                    - Available IPs: {network.num_addresses - 2}
                    - Network IP: {network.network_address}
                    - First Usable IP: {ipaddress.IPv4Network(network)[1]}
                    - Last Usable IP: {ipaddress.IPv4Network(network)[-2]}
                    - Broadcast IP: {network.broadcast_address}
                """))
                print("=" * 80, "\n")
                break
            except (ValueError, UnboundLocalError):
                print("Only valid network IP allowed (Ex:. 10.0.0.0)")
        submenu()
    elif option == 5:
        toolHeader()
        while True:
            try:
                n_networks = int(input("Number of networks to configure: "))
                if n_networks == "":
                    submenu()
                elif n_networks < 2:
                    print("Only integers greater than 1 allowed")
                else:
                    break
            except ValueError:
                print("Only integers greater than 1 allowed")
        while True:
            try:
                network_ip = input("Enter the desired initial network IP(CIDR): ")
                print()
                network = ipaddress.ip_network(network_ip)
                break
            except (ValueError, UnboundLocalError):
                print("Only valid network IP(CIDR) allowed (Ex:. 10.0.0.0/8)")
                print()
        networks = {}
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
        counter = 0
        print("=" * 80)
        while counter < n_networks: 
            print(dedent(f"""
                Network {counter+1}
                - CIDR: /{networks[list(networks)[counter]]['cidr']}
                - Subnet Mask: {networks[list(networks)[counter]]['network_mask']}
                - Network IP: {networks[list(networks)[counter]]['network_ip']}
                - First Usable IP: {networks[list(networks)[counter]]['first_ip']}
                - Last Usable IP: {networks[list(networks)[counter]]['last_ip']}
                - Broadcast IP: {networks[list(networks)[counter]]['broadcast_ip']}
                - Total Usable IPs: {networks[list(networks)[counter]]['hosts']}"""))
            counter += 1
        print()
        print("=" * 80, "\n")
        submenu()
 

    elif option == 6:
        toolHeader()
        while True:
            try:
                n_networks = int(input("Number of networks to configure: "))
                if n_networks == "":
                    submenu()
                elif n_networks < 1:
                    print("Only positive integers allowed")
                else:
                    break
            except ValueError:
                print("Only positive integers allowed")
        networks = {}
        for netw in range(n_networks):
            while True:
                try:
                    network_input = int(input(f"Hosts required for network {netw+1}: "))
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
                network0_ip = input("Enter the desired initial network IP: ")
                print()
                ip = ipaddress.IPv4Address(network0_ip)
                network0 = ipaddress.ip_network(f"{ip}/{sorted_networks[list(sorted_networks)[0]]['cidr']}")
                break
            except (ValueError, UnboundLocalError):
                print("Only valid network IP allowed (Ex:. 10.0.0.0)")
                print()
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
        print("=" * 80)
        while counter < n_networks - 1: 
            print(dedent(f"""
                Network {counter+2} ({networks[list(sorted_networks)[counter+1]]['needed_hosts']} hosts)
                - CIDR: /{networks[list(sorted_networks)[counter+1]]['cidr']}
                - Subnet Mask: {networks[list(sorted_networks)[counter+1]]['network_mask']}
                - Network IP: {networks[list(sorted_networks)[counter+1]]['network_ip']}
                - First Usable IP: {networks[list(sorted_networks)[counter+1]]['first_ip']}
                - Last Usable IP: {networks[list(sorted_networks)[counter+1]]['last_ip']}
                - Broadcast IP: {networks[list(sorted_networks)[counter+1]]['broadcast_ip']}
                - Total Usable IPs: {networks[list(sorted_networks)[counter+1]]['hosts']}"""))
            counter += 1
        print()
        print("=" * 80, "\n")
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
