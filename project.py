import ipaddress
import random
from textwrap import dedent
import hashlib
import getpass
import string
import math
import json
import os

# Garante que o programa reconhece o caminho completo de sistema do ficheiro database.json
file_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(file_dir, 'database.json')

# Lê o ficheiro database.json e inicia a variável 'database' com os utilizadores (dicionários)
with open(database_path, 'r') as f:
   database = json.load(f)

# Atualiza o ficheiro database.json com os dados atualizaos da variável 'database'
def databaseExport():
    database_export = json.dumps(database, indent=4)
    with open(database_path, "w") as f:
        f.write(database_export)

# Define as cores aplicadas no texto
red = "\033[31m"
cyan_underline = "\033[4;36m"
green_bold = "\033[1;32m"
bold = "\033[1m"
normal  = "\033[0m"

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
numbers = string.digits
special = string.punctuation

tools = [
    "   1. Conversão de IP (Decimal para Binário)", 
    "   2. Conversão de IP (Binário para Decimal)", 
    "   3. Classicação de IPs (Privado vs Público)", 
    "   4. Cálculo da Máscara de Rede/CIDR",
    "   5. Subnetting",
    "   6. VLSM",
    "",
    "=" * 62,
    "",
    "   7. Alterar Password",
    "   8. Administração de Utilizadores"
]

current_user = None

def logo():
    print("=" * 62)
    print(dedent(f"""\
 ____             _        _     _____                        
|  _ \ _   _  ___| | _____| |_  |_   _| __ __ _  ___ ___ _ __ 
| |_) | | | |/ __| |/ / _ \ __|   | || '__/ _` |/ __/ _ \ '__|
|  __/| |_| | (__|   <  __/ |_    | || | | (_| | (_|  __/ |   
|_|    \__, |\___|_|\_\___|\__|   |_||_|  \__,_|\___\___|_|   
       |___/                                                  """))

############################
### Menus and Cabeçalhos ###
############################

# Menu inicial
def mainHeader():
    print("\033c", end="")
    logo()
    print(dedent(f"""\
        {"=" * 62}
        {bold}Projeto Final Python{normal}
        {green_bold}Pycket Tracer Tools{normal} - Ferramenta de Apoio a Networking
        Diogo Fontes | Luís Oliveira
        {"=" * 62}

        {"  1. Login"}
        {"  2. Registar Utilizador"}

        {"=" * 62}
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
                print(f"{red}Insira apenas opções entre 1 e 2{normal}")
        except ValueError:
            print(f"{red}Insira apenas opções entre 1 e 2{normal}")

# Menu principal
def menu():
        print("\033c", end="")
        global option
        global current_user
        logo()
        print("=" * 62)
        if database[current_user]['role'] == 'admin':
            print()
            print(*tools,sep="\n")
            print(dedent(f"""
                {"=" * 62}
                Utilizador atual: {cyan_underline}{current_user.capitalize()}{normal} (Clique enter para terminar sessão)"""))
        else:
            print()
            # Se o utilizador não for 'admin', não tem permissão para ver e selecionar a opção 8 (Administração de Utilizadores)
            print(*tools[:-1],sep="\n")
            print(dedent(f"""
                {"=" * 62}
                Utilizador atual: {cyan_underline}{current_user.capitalize()}{normal} (Clique enter para terminar sessão)"""))
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
                        print(f"{red}Insira apenas opções entre 1 e 8{normal}")
                else:
                    if int(option) >= 1 and int(option) <= 7:
                        tool(int(option))
                    else:
                        print(f"{red}Insira apenas opções entre 1 e 7{normal}")
            except ValueError:
                print(f"{red}Insira apenas opções númericas{normal}")

# Submenu
def submenu():
    print(f"""\
    1. Voltar ao menu principal
    0. Sair
    """)
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
                print(f"{red}Insira apenas opções entre 0 e 1{normal}")
        except ValueError:
            print(f"{red}Insira apenas opções entre 0 e 1{normal}")

# Menu de administração
def administration():
    global admin_option
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        {green_bold}{"Pycket Tracer Tools"}{normal}
        Administração de Utilizadores
        {"=" * 62}

        {"  1. Registar Utilizador"}
        {"  2. Remover Utilizador"}
        {"  3. Listar Utilizadores"}
        {"  4. Alterar Passwords"}
        {"  5. Alterar Permissões"}
        
        {"=" * 62}"""))
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
                print(f"{red}Insira apenas opções entre 1 e 5{normal}")
        except ValueError:
            print(f"{red}Insira apenas opções entre 1 e 5{normal}")

# Cabeçalho e rodapé dos resultados
def resultHeaderFooter():
    print()
    print("=" * 62, "\n")

# Cabeçalho das ferramentas
def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 62}
        {green_bold}{"Pycket Tracer Tools"}{normal}
        {toolTitle[6:]}
        {"=" * 62}
        """))

##########################
### Funções Principais ###
##########################

# Função de login
## Funciona apenas para utilizadores disponiveis na variável 'database'
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
            print(f"{red}Utilizador não encontrado{normal}")
    password_check()
    global current_user
    current_user = username_input
    menu()

# Função de registo de utilizadores
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
            print(f"{red}Insira pelo menos 3 caracteres{normal}")
        else:
            break
    if username_input not in database:
        password_get()
        database[username_input] = {
            'password': hashed_password,
            'role':'user'
            }
        databaseExport()
        print(f"\n{green_bold}Login para o utilizador '{username_input}' criado com sucesso!{normal}")
        print("\nClique enter para voltar ao menu anterior")
        getpass.getpass(prompt="")
        if current_user is None:
            login()
        else:
            administration()
    else:
        print(f"{red}O utilizador {username_input} já existe{normal}")
        print("\nClique enter para voltar ao menu anterior")
        getpass.getpass(prompt="")
        if current_user is None:
            mainHeader()
        else:
            administration()

# Função de remoção de utilizadores
## Não permite a remoção do utilizador atual
## Passo de confirmação para a remoção
def removeUser():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Remover Utilizador
        {"=" * 62}
    """))
    while True:
        username_input = input("Utilizador a remover: ")
        if username_input == "":
           administration()
        elif username_input == current_user:
            print(f"{red}Não pode eliminar o utilizador atual{normal}")
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
                        databaseExport()
                        print(f"\n{green_bold}Utilizador '{username_input}' removido com sucesso!{normal}")
                        print("\nClique enter para voltar ao menu anterior")
                        getpass.getpass(prompt="")
                        administration()
                    elif int(remove_confirm) == 2:
                        administration()
                    else:
                        print(f"{red}Insira apenas opções entre 1 e 2{normal}")
                except ValueError:
                    print(f"{red}Insira apenas opções entre 1 e 2{normal}")             
        else:
            print(f"{red}Utilizador não encontrado{normal}")

# Função de alteração de password (administradores)
## Permite a alteração de passwords dos utilizadores, através de um administrador
def changePasswordAdmin():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Password
        {"=" * 62}
    """))
    while True:
        username_input = input("Alterar password para o utilizador: ")
        if username_input == "":
            administration()
        elif username_input in database:
            break
        else:
            print(f"{red}Utilizador não encontrado{normal}")
    print("*** Nova Password ***")
    password_get()
    database[username_input]['password'] = hashed_password
    databaseExport()
    print(f"\n{green_bold}A password do utilizador '{username_input}' foi atualizada com sucesso!{normal}")
    print("\nClique enter para voltar ao menu anterior")
    getpass.getpass(prompt="")
    administration()

# Função de alteração de password (utilizadores)
## Permite a alteração de password do utilizador atual
def changePassword():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Password
        {"=" * 62}
    """))
    print("*** Password Atual ***")
    password_check()
    print("*** Nova Password ***")
    password_get()
    database[current_user]['password'] = hashed_password
    databaseExport()
    print(f"\n{green_bold}A sua password foi atualizada com sucesso!{normal}")
    print("\nClique enter para voltar ao menu anterior")
    getpass.getpass(prompt="")
    menu()

# Função de alteração de permissões (administradores)
## Permite a alteração de permissões dos utilizadores, através de um administrador
def changeRole():
    print("\033c", end="")
    print(dedent(f"""
        {"=" * 62}
        Alteração de Permissões
        {"=" * 62}
    """))
    while True:
        username_input = input("Alterar permissões para o utilizador: ")
        if username_input == "":
            administration()
        elif username_input in database:
            if username_input == current_user:
                print(f"{red}Não pode alterar as permissões do utilizador atual{normal}")
            else:
                break
        else:
            print(f"{red}Utilizador não encontrado{normal}")
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
                databaseExport()
                print(f"\n{green_bold}As permissões do utilizador '{username_input}' foram alteradas com sucesso!{normal}")
                print("\nClique enter para voltar ao menu anterior")
                getpass.getpass(prompt="")
                break
            elif int(role_option) == 2:
                print(f"As permissões do utilizador '{username_input}' foram mantidas!")
                print("\nClique enter para voltar ao menu anterior")
                getpass.getpass(prompt="")
                break
            else:
                print(f"{red}Insira apenas opções entre 1 e 2{normal}")
        except ValueError:
            print(f"{red}Insira apenas opções entre 1 e 2{normal}")
    administration()

# Função de atribuição de password
## Requisitos mínimos
## Encripta a password e inicia a variável 'hashed_password' com a hash da password
def password_get():
    global hashed_password
    while True:
            password = getpass.getpass()
            if len(password) < 8:
                print(f"{red}A password tem que ter um mínimo de 8 caracteres{normal}")
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

# Função de confirmação de password
## Encripta o input, transforma-o numa hash e compara-a com a value 'password' do utilizador atual, no dictionário 'database'
## Máximo de 3 tentativas passwords incorretas
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
                    {red}Password incorreta{normal}
                    Tentativas restantes: {max_attempts - attempts}
                    {"=" * 62}
                    """))
            else:
                print(f"{red}Atingiu o número máximo de tentativas{normal}")
                print("Clique enter para sair")
                getpass.getpass(prompt="")
                exit()

# Função de conversão de IP (decimal para binário)
def decToBin():
    toolHeader()
    while True:
        try:
            decimal_ip = input("Insira um endereço de IPv4 em formato decimal: ")
            if decimal_ip == "":
                print()
                break
            else:
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimal_ip)))
                resultHeaderFooter()
                print(f"IP em formato binário: {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                resultHeaderFooter()
                break
        except ValueError:
            print(f"{red}Insira um IPv4 válido{normal} (Ex.: '{defaultDecimalIP()}')")
    submenu()

# Função de conversão de IP (binário para decimal)
def binToDec():
    toolHeader()
    while True:
        try:
            binary_ip = input("Insira um endereço de IPv4 em formato binário: ")
            if binary_ip == "":
                print()
                break
            else:
                binary_ip = binary_ip.replace(".", "")
                if len(binary_ip) == 32:
                    binary_ip = int(binary_ip, 2)
                    ip = ipaddress.IPv4Address(binary_ip)
                    resultHeaderFooter()
                    print(f"IP em formato decimal: {ip}")
                    resultHeaderFooter()
                    break
                else:
                    print(f"{red}Insira um IPv4 válido{normal} (Ex.: '{defaultBinaryIP()}')")
        except ValueError:
            print(f"{red}Insira um IPv4 válido{normal} (Ex.: '{defaultBinaryIP()}')")
    submenu()

# Função de classificação de IPs
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
                    print(f"O IP '{ip}' é multicast (Classe D)")
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
            print(f"{red}Insira um IPv4 válido{normal} (Ex.: '{defaultDecimalIP()}')")
    submenu()

# Função de cálculo da subnet/CIDR ideal
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
                # Número máximo possível de dipositivos para redes com endereços de IPv4
                if hosts < 2147483646:
                    break
                else:
                    print(f"{red}Atingiu o número máximo de endereços possíveis para redes IPv4, tente uma rede menor{normal}")
        except ValueError:
            print(f"{red}Insira apenas números inteiros{normal}")
    # Todas as redes têm de incluir 2 IPs (rede e broadcast), a adicionar aos hosts totais
    total_ips = hosts + 2
    hostID_bits = 0
    # O IPv4 é constituido por 32 bits, que são divididos entre networkID e hostID
    ## Para calcular o CIDR ideal, começamos com 32 bits no networkID
    ## O número de IPs por rede = 2^hostID bits
    ## Começando com 0 hostID bits, enquanto a cálculo anterior for inferior ao 'total_ips', incrementamos 1 bit ao hostID
    ## O CIDR é igual ao múmero de bits restantes no networkID
    while (2 ** hostID_bits) < total_ips:
        hostID_bits += 1
        cidr = 32 - hostID_bits
    while True:
        try:
            decimal_ip = input("Insira o IPv4 da rede: ")
            ip = ipaddress.IPv4Address(decimal_ip)
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
            print(f"{red}Insira um IP de rede válido{normal} (Ex:. 10.0.0.0)")
    submenu()

# Função de subnetting
def subnetting():
    toolHeader()
    while True:
        try:
            n_networks = input("Número de redes a configurar: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 2:
                print(f"{red}Insira apenas números inteiros maiores que 1{normal}")
            elif int(n_networks) > 16777216:
                print(f"{red}Atingiu o número máximo de redes possíveis para endereços IPv4{normal}")
            else:
                break
        except ValueError:
            print(f"{red}Insira apenas números inteiros maiores que 1{normal}")
    while True:
        try:
            network_ip = input("Insira o IPv4 da rede inicial (CIDR): ")
            initial_network = ipaddress.ip_network(network_ip)
            networks = {}
            n_networks = int(n_networks)
            # Calcula o número de hostID bits que vai ser necessário passar para o networkID
            ## Segue uma função logarítmica de base 2, tendo em conta o número de redes pretendida
            bits_needed = math.ceil(math.log2(n_networks))
            next_prefix = initial_network.prefixlen + bits_needed
            if next_prefix > 31:
                print(f"{red}A rede inicial não pode ser divida em {n_networks} redes{normal}")
            elif next_prefix == 31:
                subnets = list(initial_network.subnets(new_prefix=next_prefix))
                for netw in range(n_networks):
                    networks[f'network_{netw}'] = {
                        'network_mask': subnets[netw].netmask,
                        'cidr': subnets[netw].prefixlen,
                        'first_ip': subnets[netw][0],
                        'last_ip': subnets[netw].broadcast_address
                    }
                    netw += 1
                break
            else:
                subnets = list(initial_network.subnets(new_prefix=next_prefix))
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
            print(f"{red}Insira um IP de rede (CIDR) válido{normal} (Ex:. 10.0.0.0/8)")
    counter = 0
    print("=" * 62)
    if next_prefix == 31:
        while counter < n_networks: 
            print(dedent(f"""
                {cyan_underline}Network {counter+1} - Point-to-point link (RFC 3021){normal}
                - CIDR: /{networks[list(networks)[counter]]['cidr']}
                - Subnet Mask: {networks[list(networks)[counter]]['network_mask']}
                - First IP: {networks[list(networks)[counter]]['network_ip']}
                - Last IP: {networks[list(networks)[counter]]['broadcast_ip']}"""))
            counter += 1
    else:
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

# Função de VLSM
def vlsm():
    toolHeader()
    while True:
        try:
            n_networks = input("Número de redes a configurar: ")
            if n_networks == "":
                print()
                submenu()
            elif int(n_networks) < 2:
                print(f"{red}Insira apenas números inteiros maiores que 1{normal}")
            else:
                break
        except ValueError:
            print(f"{red}Insira apenas números inteiros maiores que 1{normal}")
    networks = {}
    n_networks = int(n_networks)
    for netw in range(n_networks):
        while True:
            try:
                network_input = int(input(f"Dispositivos necessários para a rede {netw+1}: "))
                if network_input < 1:
                    print(f"{red}Insira apenas números inteiros positivos{normal}")
                elif network_input > 2147483646:
                    print(f"{red}Não é possível a divisão de redes com mais de 2147483646 dispositivos{normal}")
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
                if hosts_sum > (4294967294-(n_networks*2)):
                    print(f"{red}Atingiu o número máximo de IPs possíveis para endereços de IPv4, tente uma rede menor{normal}")
                else:
                    break
            except ValueError:
                print(f"{red}Insira apenas números inteiros positivos{normal}")
    counter = 0
    while counter < n_networks:
        cidr = 0
        bits = 0
        total_ips = networks[f'network_{counter}']['needed_ips']
        while (2 ** bits) < total_ips:
            bits += 1
            cidr = (32 - bits)
        networks[f'network_{counter}']['cidr'] = cidr
        counter += 1
    sorted_networks = dict(sorted(networks.items(), reverse=True, key=lambda item: item[1]['needed_hosts']))
    while True:
        try:
            initial_network_ip = input("Insira o IPv4 da rede inicial: ")
            ip = ipaddress.IPv4Address(initial_network_ip)
            initial_network = ipaddress.ip_network(f"{ip}/{sorted_networks[list(sorted_networks)[0]]['cidr']}")
            break
        except (ValueError, UnboundLocalError):
            print(f"{red}Insira um IP de rede válido (Ex:. 10.0.0.0){normal}")
    networks[list(sorted_networks)[0]]['network_mask'] = initial_network.netmask
    networks[list(sorted_networks)[0]]['hosts'] = (initial_network.num_addresses - 2)
    networks[list(sorted_networks)[0]]['network_ip'] = initial_network.network_address
    networks[list(sorted_networks)[0]]['first_ip'] = initial_network[1]
    networks[list(sorted_networks)[0]]['last_ip'] = initial_network[-2]
    networks[list(sorted_networks)[0]]['broadcast_ip'] = initial_network.broadcast_address
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
            {cyan_underline}Rede {counter+2}{normal} ({networks[list(sorted_networks)[counter+1]]['needed_hosts']} dispositivos)
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

# Função principal
## Recebe a variável 'option' da escolha do menu principal e redireciona para a ferramenta pretendida
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
    elif option == 7:
        changePassword()
    elif option == 8:
        administration()

######################
### Outras Funções ###
######################

# Função de gerar IPs decimais aleatórios
def defaultDecimalIP():
    rand_ip = []
    for x in range(4):
        rand_ip.append(str(random.randrange(0,256)))
    return ".".join(rand_ip)

# Função de gerar IPs binários aleatórios
def defaultBinaryIP():
    rand_ip = []
    for x in range(32):
        rand_ip.append(str(random.randrange(0,2)))
    rand_ip = "".join(rand_ip)
    return f"{rand_ip[0:9]}.{rand_ip[9:17]}.{rand_ip[17:25]}.{rand_ip[25:33]}"

mainHeader()