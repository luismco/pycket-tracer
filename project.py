import ipaddress
import random
from textwrap import dedent
import hashlib
import getpass
import string
import math

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
numbers = string.digits
special = string.punctuation

database = {
    'luis': {'password': '20f15cfb78a1c83af3bd7976a78952ea1b1ed435a706bb04ba2c83c7fd0a4965', 'role': 'admin'}, 
    'diogo': {'password': '9ca6a0e5e922e01e20f11d999ecc1685e969c9acc2abc83006281c131fe22a15', 'role': 'admin'},
    'ruben': {'password': 'c1cc69e61c0f1c7ade8df0f2994e582e7c1f2c57d1ec192a0baf9f96b7739d9d', 'role': 'user'}
}

tools = [
    "   1. Conversão de IP (Decimal para Binário)", 
    "   2. Conversão de IP (Binário para Decimal)", 
    "   3. Cálculo da Máscara de Rede/CIDR", 
    "   4. Classicação de IPs (Privado vs Público)",
    "   5. Subnetting",
    "   6. VLSM",
    "",
    "=" * 62,
    "",
    "   7. Alterar Password",
    "   8. Administração de Utilizadores",
    ""
]

current_user = None

def logo():
    print("=" * 62)
    print(dedent(f"""
 ____             _        _     _____                        
|  _ \ _   _  ___| | _____| |_  |_   _| __ __ _  ___ ___ _ __ 
| |_) | | | |/ __| |/ / _ \ __|   | || '__/ _` |/ __/ _ \ '__|
|  __/| |_| | (__|   <  __/ |_    | || | | (_| | (_|  __/ |   
|_|    \__, |\___|_|\_\___|\__|   |_||_|  \__,_|\___\___|_|   
       |___/                                                  
    """))

#########################
### Menus and Headers ###
#########################
def mainHeader():
    print("\033c", end="")
    logo()
    print(dedent(f"""\
        {"=" * 62}
        \033[1m{"Projeto Final Python"}\033[0m
        \033[1;32m{"Pycket Tracer Tools"}\033[0m - Ferramenta de Apoio a Networking
        Diogo Fontes | Luís Oliveira
        {"=" * 62}

        1. Login
        2. Registar Utilizador
        """))
    while True:
        try:
            main_option = input("Selecione a opção desejada (Clique enter para sair): ")
            if main_option == "":
                exit()
            elif int(main_option) == 1:
                login()
            elif int(main_option) == 2:
                signin()
            else:
                print("Insira apenas opções entre 1 e 2")
        except ValueError:
            print("Insira apenas opções entre 1 e 2")

def menu():
        print("\033c", end="")
        global option
        global current_user
        print(dedent(f"""
            {"=" * 62}
            Pycket Tracer Tools
            {"=" * 62}"""))
        if database[current_user]['role'] == 'admin':
            print()
            print(*tools,sep="\n")
            print(dedent(f"""\
                {"=" * 62}
                Utilizador atual: \033[4;36m{current_user.capitalize()}\033[0m (Clique enter para terminar sessão)"""))
        else:
            print(*tools[:-1],sep="\n")
            print(dedent(f"""\
                {"=" * 62}
                Utilizador atual: \033[4;36m{current_user.capitalize()}\033[0m (Clique enter para terminar sessão)"""))
        while True:
            try:
                option = input("\nSelecione a ferramenta desejada: ")
                if option == "":
                    current_user = None
                    mainHeader()
                if database[current_user]['role'] == 'admin':
                    if int(option) >= 1 and int(option) <= 8:
                        tool(int(option))
                    else:
                        print("Insira apenas opções entre 1 e 8")
                else:
                    if int(option) >= 1 and int(option) <= 7:
                        tool(int(option))
                    else:
                        print("Insira apenas opções entre 1 e 7")
            except ValueError:
                print("Insira apenas opções mostradas")

def submenu():
    print(dedent(f"""\
        1. Voltar ao menu principal
        0. Sair     
        """))
    while True:
        try:
            sub_option = input("Selecione a opção desejada (Clique enter para continuar na ferramenta atual): ")
            if sub_option == "":
                tool(int(option))
            elif int(sub_option) == 1:
                menu()
            elif int(sub_option) == 0:
                exit()
            else:
                print("Insira apenas opções entre 0 e 1")
        except ValueError:
            print("Insira apenas opções entre 0 e 1")

def administration():
    global admin_option
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Administração de Utilizadores
        {"=" * 62}
        1. Registar Utilizador
        2. Remover Utilizador
        3. Listar Utilizadores
        4. Alterar Passwords
        5. Alterar Permissões
        """))
    while True:
        try:
            admin_option = input("Selecione a opção desejada (Clique enter para voltar ao menu principal): ")
            if admin_option == "":
                menu()
            elif int(admin_option) == 1:
                signin()
            elif int(admin_option) == 2:
                removeUser()
            elif int(admin_option) == 3:
                print("\033c", end="")
                print(dedent(f"""
                    {"=" * 62}
                    Lista de Utilizadores
                    {"=" * 62}
                    {list(database.keys())}"""))
                print(f"\nClique enter para voltar ao menu anterior")
                getpass.getpass(prompt="")
                administration()
            elif int(admin_option) == 4:
                changePasswordAdmin()
            elif int(admin_option) == 5:
                changeRole()
            else:
                print("Insira apenas opções entre 1 e 4")
        except ValueError:
            print("Insira apenas opções entre 1 e 4")

def resultHeaderFooter():
    print()
    print("=" * 62, "\n")

def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 62}
        \033[1;32m{"Pycket Tracer Tools"}\033[0m
        {toolTitle[6:]}
        {"=" * 62}
        """))

######################
### Main Functions ###
######################
def login():
    print("\033c", end="")
    global username_input
    print(dedent(f"""
        {"=" * 62}
        Login
        {"=" * 62}
    """))
    while True:
        username_input = input("Utilizador: ")
        if username_input == "":
           mainHeader()
        elif username_input in database:
            break
        else:
            print("Utilizador não encontrado")
    password_check()
    print(f"\nBem vindo, {username_input.capitalize()}!")
    global current_user
    current_user = username_input
    menu()

def signin():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Registar Novo Utilizador
        {"=" * 62}
    """))
    while True:          
        username_input = input("Utilizador: ")
        if username_input == "":
            if current_user is None:
                mainHeader()
            else:
                administration()
        elif len(username_input) < 3:
            print("Insira pelo menos 3 caracteres")
        else:
            break
    if username_input not in database:
        password_get()
        database[username_input] = {
            'password': hashed_password,
            'role':'user'
            }
        print(f"\nLogin para o utilizador '{username_input}' criado com sucesso!")
        print("\nClique enter para voltar ao menu anterior")
        getpass.getpass(prompt="")
        if current_user is None:
            login()
        else:
            administration()
    else:
        print(f"O utilizador {username_input} já existe")
        print("\nClique enter para voltar ao menu anterior")
        getpass.getpass(prompt="")
        if current_user is None:
            mainHeader()
        else:
            administration()

def removeUser():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Remover Utilizador
        {"=" * 62}"""))
    while True:
        username_input = input("Utilizador a remover: ")
        if username_input == "":
           administration()
        elif username_input == current_user:
            print("Não pode eliminar o utilizador atual")
        elif username_input in database:
            while True:
                try:
                    remove_confirm = input(dedent(f"""
                    Tem a certeza que quer eliminar o utlizador {username_input}?
                    1. Sim
                    2. Não

                    Selecione a opção desejada: """))
                    if int(remove_confirm) == 1:
                        database.pop(username_input)
                        print(f"\nUtilizador '{username_input}' removido com sucesso!")
                        print("\nClique enter para voltar ao menu anterior")
                        getpass.getpass(prompt="")
                        administration()
                    elif int(remove_confirm) == 2:
                        administration()
                    else:
                        print("Insira apenas opções entre 1 e 2")
                except ValueError:
                    print("Insira apenas opções entre 1 e 2")             
        else:
            print("Utilizador não encontrado")

def changePasswordAdmin():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Password
        {"=" * 62}"""))
    while True:
        username_input = input("Alterar password para o utilizador: ")
        if username_input == "":
            administration()
        elif username_input in database:
            break
        else:
            print("Utilizador não encontrado")
    print("*** Nova Password ***")
    password_get()
    database[username_input]['password'] = hashed_password
    print(f"\nA password do utilizador '{username_input}' foi atualizada com sucesso!")
    print("\nClique enter para voltar ao menu anterior")
    getpass.getpass(prompt="")
    administration()

def changePassword():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Password
        {"=" * 62}"""))
    print("*** Password Atual ***")
    password_check()
    print("*** Nova Password ***")
    password_get()
    database[current_user]['password'] = hashed_password
    print(f"\nA sua password foi atualizada com sucesso!")
    print("\nClique enter para voltar ao menu anterior")
    getpass.getpass(prompt="")
    menu()

def changeRole():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Permissões
        {"=" * 62}"""))
    while True:
        username_input = input("Alterar permissões para o utilizador: ")
        if username_input == "":
            administration()
        elif username_input in database:
            if username_input == current_user:
                print("Não pode alterar as permissões do utilizador atual")
            else:
                break
        else:
            print("Utilizador não encontrado")
    current_role = database[username_input]['role']
    if current_role == 'admin':
        new_role = 'user'
    else:
        new_role = 'admin'
    print(dedent(f"""
        *** Permissões Atuais ***
        Utilizador: {username_input}
        Permissões: {current_role}\n
        1. Alterar permissões ({current_role} para {new_role})
        2. Manter permissões ({current_role})
        """))
    while True:
        try:
            role_option = input("Selecione a opção desejada: ")
            if int(role_option) == 1:
                database[username_input]['role'] = new_role
                print(f"\nAs permissões do utilizador '{username_input}' foram alteradas com sucesso!")
                print("\nClique enter para voltar ao menu anterior")
                getpass.getpass(prompt="")
                break
            elif int(role_option) == 2:
                print(f"As permissões do utilizador '{username_input}' foram mantidas!")
                print("\nClique enter para voltar ao menu anterior")
                getpass.getpass(prompt="")
                break
            else:
                print("Insira apenas opções entre 1 e 2")
        except ValueError:
            print("Insira apenas opções entre 1 e 2")
    administration()

def password_get():
    global hashed_password
    while True:
            password = getpass.getpass()
            if len(password) < 8:
                print("A password tem que ter um mínimo de 8 caracteres")
            else:
                lowercase_check = False
                uppercase_check = False
                numbers_check = False
                special_check = False
                for char in password:
                    if char in lowercase:
                        lowercase_check = True
                    elif char in uppercase:
                        uppercase_check = True
                    elif char in numbers:
                        numbers_check = True
                    elif char in special:
                        special_check = True
                if all([lowercase_check, uppercase_check, numbers_check, special_check]):
                    break
                else:
                    print(dedent(f"""
                        *** Requisitos de Password ***
                        A password deve conter letras minúsculas, maiúsculas, números e caracteres especias ({special})
                        """))
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

def password_check():
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        password_input = getpass.getpass()
        hashed_input_password = hashlib.sha256(password_input.encode()).hexdigest()
        if database[username_input]['password'] == hashed_input_password:
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print(dedent(f"""
                    {"=" * 62}
                    Password incorreta
                    Tentativas restantes: {max_attempts - attempts}
                    {"=" * 62}
                    """))
            else:
                print("Atingiu o número máximo de tentativas")
                print("Clique enter para sair")
                getpass.getpass(prompt="")
                exit()

def decToBin():
    toolHeader()
    while True:
        try:
            decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
            if decimalIP == "":
                print()
                break
            else:
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                resultHeaderFooter()
                print(f"IP em formato binário: {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                resultHeaderFooter()
                break
        except ValueError:
            print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
    submenu()

def binToDec():
    toolHeader()
    while True:
        try:
            binaryIP = input("Insira um endereço de IPv4 em formato binário: ")
            if binaryIP == "":
                print()
                break
            else:
                binaryIP = binaryIP.replace(".", "")
                if len(binaryIP) == 32:
                    binaryIP = int(binaryIP, 2)
                    ip = ipaddress.IPv4Address(binaryIP)
                    resultHeaderFooter()
                    print(f"IP em formato decimal: {ip}")
                    resultHeaderFooter()
                    break
                else:
                    print(f"Insira um IPv4 válido (Ex.: '{defaultBinaryIP()}')")
        except ValueError:
            print(f"Insira um IPv4 válido (Ex.: '{defaultBinaryIP()}')")
    submenu()

def subnetCIDR():
    toolHeader()
    while True:
        try:
            hosts = input("Insira o número de dispositivos necessários: ")
            if hosts == "":
                print()
                submenu()
            else:
                hosts = int(hosts)
                break
        except ValueError:
            print("Insira apenas números inteiros")
    totalHosts = hosts + 2
    bits = 0
    while (2 ** bits) < totalHosts:
        bits += 1
        cidr = 32 - bits
    while True:
        try:
            decimalIP = input("Insira o IPv4 da rede: ")
            ip = ipaddress.IPv4Address(decimalIP)
            network = ipaddress.ip_network(f"{ip}/{cidr}")
            resultHeaderFooter()
            print(dedent(f"""\
                - Máscara de Rede Adequeada: {network.netmask}
                - CIDR adequado: /{cidr}
                - Número de IPs disponíveis: {network.num_addresses - 2}
                - IP da rede: {network.network_address}
                - Primero IP Disponível: {ipaddress.IPv4Network(network)[1]}
                - Último IP Disponível: {ipaddress.IPv4Network(network)[-2]}
                - IP de Broadcast: {network.broadcast_address}"""))
            resultHeaderFooter()
            break
        except (ValueError, UnboundLocalError):
            print("Insira um IP de rede válido (Ex:. 10.0.0.0)")
    submenu()

def ipClass():
    toolHeader()
    while True:
        try:
            ip = input("Insira um endereço de IPv4 (Decimal): ")
            if ip == "":
                print()
                break
            else:
                if ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('0.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('127.255.255.255'):
                    ip_class = str("Classe A")
                elif ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('128.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('191.255.255.255'):
                    ip_class = str("Classe B")
                elif ipaddress.IPv4Address(ip) > ipaddress.IPv4Address('192.0.0.0') and ipaddress.IPv4Address(ip) < ipaddress.IPv4Address('223.255.255.255'):
                    ip_class = str("Classe C")
                if ipaddress.IPv4Address(ip).is_reserved is True:
                    resultHeaderFooter()
                    print(f"O IP '{ip}' é reservado (Classe E)")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_link_local is True:
                    resultHeaderFooter()
                    print(f"O IP '{ip}' é link local")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_loopback is True:
                    resultHeaderFooter()
                    print(f"O IP '{ip}' é loopback")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_multicast is True:
                    resultHeaderFooter()
                    print(f"The IP '{ip}' é multicast (Classe D)")
                    resultHeaderFooter()
                    break
                elif ipaddress.IPv4Address(ip).is_private is True:
                    resultHeaderFooter()
                    print(f"O IP '{ip}' é privado ({ip_class})")
                    resultHeaderFooter()
                    break
                else:
                    resultHeaderFooter()
                    print(f"O IP '{ip}' é público ({ip_class})")
                    resultHeaderFooter()
                    break
        except ValueError:
            print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
    submenu()

def subnetting():
    toolHeader()
    while True:
        try:
            n_networks = input("Número de redes a configurar: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 2:
                print("Insira apenas números inteiros maiores que 1")
            else:
                break
        except ValueError:
            print("Insira apenas números inteiros maiores que 1")
    while True:
        try:
            network_ip = input("Insira o IPv4 da rede inicial (CIDR): ")
            print()
            network = ipaddress.ip_network(network_ip)
            break
        except (ValueError, UnboundLocalError):
            print("Insira um IP de rede (CIDR) válido (Ex:. 10.0.0.0/8)")
            print()
    networks = {}
    n_networks = int(n_networks)
    bits_needed = math.ceil(math.log2(n_networks))
    new_prefix = network.prefixlen + bits_needed
    subnets = list(network.subnets(new_prefix=new_prefix))
    for netw in range(int(n_networks)):
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
    print("=" * 62)
    while counter < n_networks: 
        print(dedent(f"""
            \033[4;36m{"Rede"} {counter+1}\033[0m
            - CIDR: /{networks[list(networks)[counter]]['cidr']}
            - Máscara de Rede: {networks[list(networks)[counter]]['network_mask']}
            - IP da Rede: {networks[list(networks)[counter]]['network_ip']}
            - Primeiro IP Disponível: {networks[list(networks)[counter]]['first_ip']}
            - Último IP Disponível: {networks[list(networks)[counter]]['last_ip']}
            - IP de Broadcast: {networks[list(networks)[counter]]['broadcast_ip']}
            - Número Total de IPs: {networks[list(networks)[counter]]['hosts']}"""))
        counter += 1
    resultHeaderFooter()
    submenu()

def vlsm():
    toolHeader()
    while True:
        try:
            n_networks = input("Número de redes a configurar: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 1:
                print("Insira apenas números inteiros positivos")
            else:
                break
        except ValueError:
            print("Insira apenas números inteiros positivos")
    networks = {}
    n_networks = int(n_networks)
    for netw in range(n_networks):
        while True:
            try:
                network_input = int(input(f"Dispositivos necessários para a rede {netw+1}: "))
                if network_input < 1:
                    print("Insira apenas números inteiros positivos")
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
                print("Insira apenas números inteiros positivos")
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
            network0_ip = input("Insira o IPv4 da rede inicial: ")
            print()
            ip = ipaddress.IPv4Address(network0_ip)
            network0 = ipaddress.ip_network(f"{ip}/{sorted_networks[list(sorted_networks)[0]]['cidr']}")
            break
        except (ValueError, UnboundLocalError):
            print("Insira um IP de rede válido (Ex:. 10.0.0.0)")
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
    print("=" * 62)
    while counter < n_networks - 1: 
        print(dedent(f"""
            \033[4;36m{"Rede"} {counter+2}\033[0m ({networks[list(sorted_networks)[counter+1]]['needed_hosts']} dispositivos)
            - CIDR: /{networks[list(sorted_networks)[counter+1]]['cidr']}
            - Máscara de Rede: {networks[list(sorted_networks)[counter+1]]['network_mask']}
            - Rede de IP: {networks[list(sorted_networks)[counter+1]]['network_ip']}
            - Primeiro IP Disponível: {networks[list(sorted_networks)[counter+1]]['first_ip']}
            - Último IP Disponível: {networks[list(sorted_networks)[counter+1]]['last_ip']}
            - IP de Broadcast: {networks[list(sorted_networks)[counter+1]]['broadcast_ip']}
            - Número Total de IPs Disponíveis: {networks[list(sorted_networks)[counter+1]]['hosts']}
        """))
        counter += 1
    print("=" * 62, "\n")
    submenu()

def tool(option):
    print("\033c", end="")
    if option == 1:
        decToBin()
    elif option == 2:
        binToDec()
    elif option == 3:
        subnetCIDR()
    elif option == 4:
        ipClass()
    elif option == 5:
        subnetting()
    elif option == 6:
        vlsm()
    elif option == 7:
        changePassword()
    elif option == 8:
        administration()

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

mainHeader()