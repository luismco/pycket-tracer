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

tools = ["1. Conversão de IP (Decimal para Binário)", 
         "2. Conversão de IP (Binário para Decimal)", 
         "3. Cálculo da Máscara de Rede/CIDR", 
         "4. Classicação de IPs (Privado vs Público)",
         "5. Alterar Password",
         "6. Terminar sessão",
         "7. Administração de Utilizadores"
        ]

current_user = None


#########################
### Menus and Headers ###
#########################

def mainHeader():
    print(dedent(f"""\
        {"=" * 50}
        Projeto Final Python
        Pycket Tracer - Ferramenta de Apoio a Networking
        Diogo Fontes | Luís Oliveira
        {"=" * 50}
        1. Login
        2. Registar Novo Utilizador
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
        global option
        print(dedent(f"""
            {"=" * 50}
            Pycket Tracer Tools
            {"=" * 50}"""))
        if database[current_user]['role'] == 'admin': 
            print(*tools,sep="\n")
        else:
            print(*tools[:-1],sep="\n")
        while True:
            try:
                option = input("\nSelecione a ferramenta desejada (Clique enter para sair): ")
                if option == "":
                    exit()
                if database[current_user]['role'] == 'admin':
                    if int(option) >= 1 and int(option) <= 7:
                        tool(int(option))
                    else:
                        print("Insira apenas opções entre 1 e 7")
                else:
                    if int(option) >= 1 and int(option) <= 6:
                        tool(int(option))
                    else:
                        print("Insira apenas opções entre 1 e 6")
            except ValueError:
                print("Insira apenas opções mostradas")

def submenu():
    print(dedent(f"""\
        1. Voltar ao menu inicial
        0. Sair     
        """))
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

def administration():
    print(dedent(f"""
        {"=" * 50}
        Administração de Utilizadores
        {"=" * 50}
        1. Adicionar Utilizador
        2. Remover Utilizador
        3. Listar Utilizadores
        4. Alterar Passwords
        5. Alterar Permissões
        """))
    while True:
        try:
            main_option = input("Selecione a opção desejada (Clique enter para voltar ao menu principal): ")
            if main_option == "":
                menu()
            elif int(main_option) == 1:
                signin()
            elif int(main_option) == 2:
                removeUser()
            elif int(main_option) == 3:
                print(dedent(f"""
                    {"=" * 50}
                    Lista de Utilizadores
                    {"=" * 50}
                    {list(database.keys())}"""))
                input("\nClique enter para voltar ao menu anterior")
                administration()
            elif int(main_option) == 4:
                changePasswordAdmin()
            elif int(main_option) == 5:
                changeRole()
            else:
                print("Insira apenas opções entre 1 e 4")
        except ValueError:
            print("Insira apenas opções entre 1 e 4")

def resultHeader():
    print(dedent(f"""
        {"=" * 50}
        *** Resultado ***"""))

def toolHeader():
    toolTitle = tools[int(option)-1]
    print(dedent(f"""
        {"=" * 50}
        Pycket Tracer Tools
        {toolTitle[3:]}
        {"=" * 50}
        """))


######################
### Main Functions ###
######################

def login():
    global username_input
    print(dedent(f"""
        {"=" * 50}
        Login
        {"=" * 50}"""))
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
    print(dedent(f"""
        {"=" * 50}
        Registar Novo Utilizador
        {"=" * 50}"""))
    while True:           
        username_input = input("Utilizador: ")
        if username_input == "" or len(username_input) < 3:
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
        if current_user is None:
            login()
        else:
            administration()
    else:
        print(f"O utilizador {username_input} já existe")
        input("\nClique enter para voltar ao menu anterior")
        if current_user is None:
            mainHeader()
        else:
            administration()

def removeUser():
    print(dedent(f"""
        {"=" * 50}
        Remover Utilizador
        {"=" * 50}"""))
    print(current_user)
    while True:
        username_input = input("Utilizador a remover: ")
        if username_input == "":
           exit()
        elif username_input == current_user:
            print("Não pode eliminar o utilizador atual")
        elif username_input in database:
            while True:
                try:
                    remove_confirm = input(dedent(f"""
                    Tem a certeza que quer eliminar o utlizador {username_input}?
                    1. Sim
                    2. Não
                    """))
                    if int(remove_confirm) == 1:
                        database.pop(username_input)
                        administration()
                    else:
                        administration()
                except ValueError:
                    print("Insira apenas opções entre 1 e 2")
                
        else:
            print("Utilizador não encontrado")

def changePasswordAdmin():
    print(dedent(f"""
        {"=" * 50}
        Alteração de Password
        {"=" * 50}"""))
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
    administration()

def changePassword():
    print(dedent(f"""
        {"=" * 50}
        Alteração de Password
        {"=" * 50}"""))
    print("*** Password Atual ***")
    password_check()
    print("*** Nova Password ***")
    password_get()
    database[current_user]['password'] = hashed_password
    print(f"\nA sua password foi atualizada com sucesso!")
    menu()
        
def changeRole():
    print(dedent(f"""
        {"=" * 50}
        Alteração de Permissões
        {"=" * 50}"""))
    while True:
        username_input = input("Alterar permissões para o utilizador: ")
        if username_input == "":
            administration()
        elif username_input in database:
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
                break
            elif int(role_option) == 2:
                print(f"As permissões do utilizador '{username_input}' foram mantidas!")
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
    password = password.encode()
    sha256 = hashlib.sha256()
    sha256.update(password)
    hashed_password = sha256.hexdigest()

def password_check():
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        password_input = getpass.getpass().encode()
        sha256 = hashlib.sha256()
        sha256.update(password_input)
        hashed_input_password = sha256.hexdigest()
        if database[username_input]['password'] == hashed_input_password:
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print(dedent(f"""
                    {"=" * 50}
                    Password incorreta
                    Tentativas restantes: {max_attempts - attempts}
                    {"=" * 50}
                    """))
            else:
                print("Atingiu o número máximo de tentativas")
                while True:
                    try:
                        exit_input = input("Clique enter para sair")
                        if exit_input == "":
                            exit()
                        else:
                            print("Atingiu o número máximo de tentativas")
                    except ValueError:
                        print("Atingiu o número máximo de tentativas")

def tool(option):
    if option == 1:
        toolHeader()
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                resultHeader()
                print(f"IP em formato binário: {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                print("=" * 50, "\n")
                submenu()
            except ValueError:
                print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
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
                print("=" * 50, "\n")
                submenu()
            except ValueError:
                print(f"Insira um IPv4 válido (Ex.: '{defaultBinaryIP()}')")
    elif option == 3:
        toolHeader()
        while True:
            try:
                hosts = int(input("Insira o número de dispositivos necessários: "))
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
                    resultHeader()
                    print(dedent(f"""\
                    Máscara de Rede Adequeada: {network.netmask}
                    CIDR adequado: /{cidr}
                    Número de IPs disponíveis: {network.num_addresses - 2}
                    IP da rede: {network.network_address}
                    Primero IP Disponível: {ipaddress.IPv4Network(network)[1]}
                    Último IP Disponível: {ipaddress.IPv4Network(network)[-2]}
                    IP de Broadcast: {network.broadcast_address}"""))
                    print("=" * 50, "\n")
                    submenu()
                except (ValueError, UnboundLocalError):
                    print("Insira um IP de rede válido (Ex:. 10.0.0.0)")
    elif option == 4:
        toolHeader()
        while True:
            try:
                ip = input("Insira um endereço de IPv4: ")
                if ipaddress.IPv4Address(ip).is_private is True:
                    resultHeader()
                    print(f"O IP '{ip}' é um IP Privado")
                    print("=" * 50, "\n")
                    submenu()
                else:
                    resultHeader()
                    print(f"O IP '{ip}' é um IP Público")
                    print("=" * 50, "\n")
                    submenu()
            except ValueError:
                print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
    elif option == 5:
        changePassword()
    elif option == 6:
        mainHeader()
    elif option == 7:
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