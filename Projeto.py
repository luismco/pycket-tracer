import ipaddress
reguaList = [128,64,32,16,8,4,2,1]
tools = ["1. Conversão de IP (Decimal para Binário)", 
         "2. Conversão de IP (Binário para Decimal)", 
         "3. Cálculo da Máscara de Rede/CIDR", 
         "4. Classicação de IPs (Privado vs Público)", 
         "5. Régua de Bits"
         ]

def mainHeader():
    print("=" * 50)
    print("Projeto Final Python\nPycket Tracer - Ferramenta de Apoio a Networking\nDiogo Fontes | Luís Oliveira")

def resultHeader():
    print()
    print("=" * 50)
    print("Resultado")

def resultFooter():
    print("=" * 50 ,"\n")
    submenu()

def toolHeader():
    print()
    print("=" * 50)
    print("Pycket Tracer Tools")
    print(tools[int(option)-1])
    print("=" * 50)

def tool(option):
    if option == 1:
        toolHeader()
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                resultHeader()
                print(f"IP em formato binário: {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                resultFooter()
            except ValueError:
                print("Insira um IPv4 válido (Ex.: 192.168.1.1)")
    elif option == 2:
        toolHeader()
        while True:
            try:
                binaryIP = input("Insira um endereço de IPv4 em formato binário: ")
                binaryIP = binaryIP.replace(".", "")
                binaryIP = int(binaryIP, 2)
                ip = ipaddress.IPv4Address(binaryIP)
                resultHeader()
                print(f"IP em formato decimal: {ip}")
                resultFooter()
            except ValueError:
                print("Insira um IPv4 válido (Ex.: 11000000.10101000.00000001.00000001)")
    elif option == 3:
        toolHeader()
        while True:
            try:
                hosts = int(input("Insira o número de dispositivos necessários: "))
                totalHosts = hosts + 2
                bits = 0
                while (2 ** bits) < totalHosts:
                    bits += 1
                cidr = 32 - bits
                network = ipaddress.ip_network(f"192.168.0.0/{cidr}")
                resultHeader()
                print(f"Máscara de Rede Adequeada: {network.netmask}")
                print(f"CIDR adequado: /{cidr}")
                print(f"Número de IPs disponíveis: {network.num_addresses - 2}")
                resultFooter()
            except ValueError:
                print("Insira um número inteiro")
    elif option == 4:
        toolHeader()
        while True:
            try:
                ip = input("Insira um endereço de IPv4: ")
                if ipaddress.IPv4Address(ip).is_private is True:
                    resultHeader()
                    print(f"O IP '{ip}' é um IP Privado")
                    resultFooter()
                else:
                    resultHeader()
                    print(f"O IP '{ip}' é um IP Público")
                    resultFooter()
            except ValueError:
                print("Insira um IPv4 válido (Ex.: 192.168.1.1)")
    elif option == 5:
        toolHeader()
        print(reguaList)
        print("=" * 50 ,"\n")
        submenu()

def menu():
        global option
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("=" * 50)
        print(*tools,sep="\n")
        while True:
            try:
                option = input("Selecione a ferramenta desejada (Clique enter para sair): ")
                if option == "":
                    exit()
                elif int(option) >= 1 and int(option) <= 5:
                    tool(int(option))
                else:
                    print("Insira apenas opções entre 1 e 5")
            except ValueError:
                print("Insira apenas opções entre 1 e 5")

def submenu():
    print("1. Voltar ao menu inicial")
    print("0. Sair")
    while True:
        try:
            subOption = input("Selecione a opção desejada (Clique enter para continuar na ferramenta atual): ")
            if subOption == "":
                print()
                tool(int(option))
            elif int(subOption) == 1:
                print()
                menu()
            elif int(subOption) == 0:
                exit()
            else:
                print("Insira apenas opções entre 0 e 1")
        except ValueError:
            print("Insira apenas opções entre 0 e 1")

mainHeader()
menu()