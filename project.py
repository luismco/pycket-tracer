import ipaddress
import random
from textwrap import dedent
import hashlib
import getpass
import string

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
    "=" * 60,
    "",
    "   7. Alterar Password",
    "   8. Administração de Utilizadores",
    ""
]

current_user = None

#########################
### Menus and Headers ###
#########################
def mainHeader():
    print("\033c", end="")
    print(dedent(f"""\
        {"=" * 60}
        Projeto Final Python
        \033[32m{"Pycket Tracer"}\033[0m - Ferramenta de Apoio a Networking
        Diogo Fontes | Luís Oliveira
        {"=" * 60}

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
            {"=" * 60}
            Pycket Tracer Tools
            {"=" * 60}"""))
        if database[current_user]['role'] == 'admin':
            print()
            print(*tools,sep="\n")
            print(dedent(f"""\
                {"=" * 60}
                Utilizador atual: \033[4;36m{current_user.capitalize()}\033[0m (Clique enter para terminar sessão)"""))
        else:
            print(*tools[:-1],sep="\n")
            print(dedent(f"""\
                {"=" * 60}
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
        {"=" * 60}
        Administração de Utilizadores
        {"=" * 60}
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
                    {"=" * 60}
                    Lista de Utilizadores
                    {"=" * 60}
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
    print("=" * 60, "\n")

def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 60}
        Pycket Tracer Tools
        {toolTitle[3:]}
        {"=" * 60}
        """))

######################
### Main Functions ###
######################
def login():
    print("\033c", end="")
    global username_input
    print(dedent(f"""
        {"=" * 60}
        Login
        {"=" * 60}
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
        {"=" * 60}
        Registar Novo Utilizador
        {"=" * 60}
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
        {"=" * 60}
        Remover Utilizador
        {"=" * 60}"""))
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
        {"=" * 60}
        Alteração de Password
        {"=" * 60}"""))
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
        {"=" * 60}
        Alteração de Password
        {"=" * 60}"""))
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
        {"=" * 60}
        Alteração de Permissões
        {"=" * 60}"""))
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
                    {"=" * 60}
                    Password incorreta
                    Tentativas restantes: {max_attempts - attempts}
                    {"=" * 60}
                    """))
            else:
                print("Atingiu o número máximo de tentativas")
                print("Clique enter para sair")
                getpass.getpass(prompt="")
                exit()

def subnetting():
    print("Subnetting")

def vlsm():
    print("VLSM")

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