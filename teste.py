import ipaddress

hosts = int(input("Insira o número de dispositivos necessários: "))
decimalIP = input("Insira um endereço de IPv4 dentro da rede: ")
ip = ipaddress.IPv4Address(decimalIP)
totalHosts = hosts + 2
bits = 0
while (2 ** bits) < totalHosts:
    bits += 1
cidr = 32 - bits
network = ipaddress.ip_network(f"{ip}/{cidr}")
print(f"""
    Máscara de Rede Adequeada: {network.netmask}
    CIDR adequado: /{cidr}
    Número de IPs disponíveis: {network.num_addresses - 2}
    IP da rede: {network.network_address}
    Primero IP Disponível: {ipaddress.IPv4Network(network)[1]}
    Último IP Disponível: {ipaddress.IPv4Network(network)[-2]}
    IP de Broadcast: {network.broadcast_address}""")