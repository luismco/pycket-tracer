### Import dos módulos necessários ###
# Os módulos são bibliotecas de comandos e funções que não são nativas do Python #
import ipaddress #módulo adiciona todos os comandos sobre IPs e Subnets
import random #módulo para criar randoms 
from textwrap import dedent #módulo que permite imprimir em várias linhas de uma forma mais clean
import hashlib #módulo que adicina os comandos para encriptar strings
import getpass #módulo que permite pedir uma password sem que o que o utilizador escreve apareça no ecrã
import string #módulo que adiciona bibliotecas de caracteres

lowercase = string.ascii_lowercase #cria uma variável com todas as letras minúsculas
uppercase = string.ascii_uppercase #cria uma variável com todas as letras maiúsculas
numbers = string.digits #cria uma variável com todos os digitos
special = string.punctuation #cria uma variável com todos os caracteres especiais

### Cria uma variável que vai guardar os utilizadores, passwords (encriptadas) e permissões
### Começa com estes 3 users para se conseguir entrar na aplicação
### Mesmo que cries ou elimines utilizadores, sempre que o programa é reiniciado, apenas vão existir estes utilizadores
#porque o python não tem "memória"
### Este tipo de variável é um dicionário, neste caso é um "Nested Dictionary"
#basicamente são dicionário dentro de dicionários
#o dicionário principal é a variável "database" e cada utilizador é um dicionário secundário
database = {
    'luis': {'password': '20f15cfb78a1c83af3bd7976a78952ea1b1ed435a706bb04ba2c83c7fd0a4965', 'role': 'admin'}, 
    'diogo': {'password': '9ca6a0e5e922e01e20f11d999ecc1685e969c9acc2abc83006281c131fe22a15', 'role': 'admin'},
    'ruben': {'password': 'c1cc69e61c0f1c7ade8df0f2994e582e7c1f2c57d1ec192a0baf9f96b7739d9d', 'role': 'user'}
    }

### Cria uma variável que vai conter as opções do menu principal do programa
### Esta variável é um lista, cada elemento da lista é separado por virgula
#neste caso estão em linhas diferentes para o cófigo ficar mais percetível
tools = ["1. Conversão de IP (Decimal para Binário)", 
         "2. Conversão de IP (Binário para Decimal)", 
         "3. Cálculo da Máscara de Rede/CIDR", 
         "4. Classicação de IPs (Privado vs Público)",
         "5. Alterar Password",
         "6. Terminar sessão",
         "7. Administração de Utilizadores"
        ]

### Inicia a variável current_user como vazia, vai ser importante mais à frente
current_user = None


#########################
### Menus and Headers ###
#########################

### Define o primeiro menu que aparece ao utilizador
### Como é um coisa que queremos que apareça muitas vezes ao utilizador
#definimos tudo dentro de uma função com "def nome_da_função():"
### Sempre que chamarmos esta função noutro local qualquer com "nome_da_função()"
#todo este código vai correr
def mainHeader():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""\
        {"=" * 50}
        Projeto Final Python
        Pycket Tracer - Ferramenta de Apoio a Networking
        Diogo Fontes | Luís Oliveira
        {"=" * 50}
        1. Login
        2. Registar Novo Utilizador
        """)) #faz um print com as opções deste menu. O "dedent" faz com que seja possível imprimir em linhas separadas sem criar indentamento no terminal
    while True: #ciclo while True (ciclo infinito)
        try: #vai tentar o próximo código até que se chegue a um dos ifs
            main_option = input("Selecione a opção desejada (Clique enter para sair): ")
            if main_option == "": #se clicar enter
                exit() #sai do programa
            elif int(main_option) == 1: #se escrever "1"
                login() #vai para a função do login
            elif int(main_option) == 2: #se escrever "2"
                signin() #vai para a função de registar utilizadores
            else: #se for outro número qualquer
                print("Insira apenas opções entre 1 e 2") #avisa o utilizador das opções permitidas
        except ValueError: #se o utilziador introduzir uma letra qualquer iria dar um "ValueError" e encerrar o programa
            print("Insira apenas opções entre 1 e 2") #o except vai permitir que o código volte ao inicio do loop em vez de fechar o programa com o erro
        ### Como todas as opções vão dar a outra função, não precisamos de usar "break"

### Define o menu principal com as opções todas
def menu():
        print("\033c", end="") #faz clear ao terminal
        global option #fazemos com que a variabel "option", que vai ser definida aqui nesta função, possa ser usada globalmente
        print(dedent(f"""
            {"=" * 50}
            Pycket Tracer Tools
            {"=" * 50}""")) #faz o print do cabeçalho
        if database[current_user]['role'] == 'admin': #se o utilizador atual for admin vai imprimir a variável tools toda
            print(*tools,sep="\n") #imprime os elementos da lista tools, um em cada linha (\n). O "*" faz o mesmo que o .join()
        else: #se não for admin
            print(*tools[:-1],sep="\n") #imprime tudo menos o último item, que queremos que seja exclusivo aos admins
        while True: #depois de imprimir as opções, outro loop infinito para escolher a opção
            try:
                option = input("\nSelecione a ferramenta desejada (Clique enter para sair): ")
                if option == "": #se clicar enter
                    exit() #sai do programa
                if database[current_user]['role'] == 'admin': #se for admin
                    if int(option) >= 1 and int(option) <= 7: #vai ser possível escolher de 1 a 7
                        tool(int(option)) #vai para a função tool mas vamos mandar a nossa opção juntamente
                    else: #outros números
                        print("Insira apenas opções entre 1 e 7") #avisa o utilizador das opções permitidas
                else: #se não for admin
                    if int(option) >= 1 and int(option) <= 6: #só vai ser possível escolher de 1 a 6
                        tool(int(option)) #exatamente igual ao de cima
                    else: #outros números
                        print("Insira apenas opções entre 1 e 6") #avisa o utilizador das opções permitidas
            except ValueError: #se der ValuerError
                print("Insira apenas opções mostradas") #avisa o utilizador das opções permitidas
            ### Aqui foi necessário separa os inputs dos admins e outros porque por exemplo
            #mesmo não aparecendo visualmente a opção 7 aos não admin, se ele escrevessem "7"
            #iam na mesma ter acesso a essa opção
            ### A opção escolhida fica guardada na variável "option", para podermos usar depois

### Define o submenu que permite voltar atrás de cada uma das opções
def submenu():
    print(dedent(f"""\
        1. Voltar ao menu principal
        0. Sair     
        """)) #faz o print do cabeçalho com as opções
    while True: #depois de imprimir as opções, outro loop infinito para escolher a opção
        try:
            sub_option = input("Selecione a opção desejada (Clique enter para continuar na ferramenta atual): ")
            if sub_option == "": #se clicar enter
                tool(int(option)) #continua na ferramenta atual, como não mudamos a variavél "opção", vai para a mesma ferramenta
            elif int(sub_option) == 1: #se escrever "1"
                menu() #volta ao menu principal
            elif int(sub_option) == 0: #se escrever "0"
                exit() #sai do programa
            else: #outro número qualquer
                print("Insira apenas opções entre 0 e 1") #avisa o utilizador das opções permitidas
        except ValueError: #se ValueError
            print("Insira apenas opções entre 0 e 1") #avisa o utilizador das opções permitidas

### Define o menu de administração (exclusivo aos admins)
def administration():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Administração de Utilizadores
        {"=" * 50}
        1. Adicionar Utilizador
        2. Remover Utilizador
        3. Listar Utilizadores
        4. Alterar Passwords
        5. Alterar Permissões
        """)) #faz o print do cabeçalho com as opções
    while True: #depois de imprimir as opções, outro loop infinito para escolher a opção
        try:
            main_option = input("Selecione a opção desejada (Clique enter para voltar ao menu principal): ")
            if main_option == "": #se clicar enter
                menu() #volta ao menu principal
            elif int(main_option) == 1: #se escrever "1"
                signin() #vai para a função de registar utilizadores
            elif int(main_option) == 2: #se escrever "2"
                removeUser() #vai para a função de remover utilizadores
            elif int(main_option) == 3: #se escrever "3"
                print("\033c", end="")
                print(dedent(f"""
                    {"=" * 50}
                    Lista de Utilizadores
                    {"=" * 50}
                    {list(database.keys())}""")) #faz uma lista dos elementos (keys) do dicionário (database)
                    # se fosse sem o "list", imprimia isto (dict_keys(['luis', 'diogo', 'ruben'])) que não é tão visual
                input("\nClique enter para voltar ao menu anterior") #espero por um input qualquer
                administration() #redireciona para o menu anterior
            elif int(main_option) == 4: #se escrever "4"
                changePasswordAdmin() #vai para a função de alterar passwords de outros utilizadores
            elif int(main_option) == 5: #se escrever "5"
                changeRole() #vai para a função de mudar as permissões dos utilizadores
            else: #outro número qualquer
                print("Insira apenas opções entre 1 e 4") #avisa o utilizador das opções permitidas
        except ValueError: #se ValueError
            print("Insira apenas opções entre 1 e 4") #avisa o utilizador das opções permitidas

### Define o cabeçalho do resultado das ferramentas de IP
### Se definirmos aqui, não precisamos de repetir este código para cada uma das ferramentas
def resultHeader():
    print(dedent(f"""
        {"=" * 50}
        *** Resultado ***"""))

### Define o cabeçalho das ferramentas de IP
### Se definirmos aqui, não precisamos de repetir este código para cada uma das ferramentas
def toolHeader():
    toolTitle = tools[int(option)-1] #vai à lista tools e imprimir o número da opção que estamos
    ### tem o "-1" porque o index começa no "0", mas as nossas ferramentas são do 1 ao 7
    print(dedent(f"""
        {"=" * 50}
        Pycket Tracer Tools
        {toolTitle[3:]}
        {"=" * 50}
        """)) #Imprime o titulo que escolhemos atrás mas retira os primeiros 3 caracteres
    ### Passa de "1. Conversão de IP (Decimal para Binário)" para "Conversão de IP (Decimal para Binário)"


######################
### Main Functions ###
######################

### Define a função de login
def login():
    print("\033c", end="") #faz clear ao terminal
    global username_input #queremos usar esta variável globalmente
    print(dedent(f"""
        {"=" * 50}
        Login
        {"=" * 50}""")) #Imprime cabeçalho
    while True: #loop infinito para garantir que o user existe
        username_input = input("Utilizador: ")
        if username_input == "": #se clicar enter
           mainHeader() #voltar ao menu inicial
        elif username_input in database: #se o utilizador já existir na database
            break #sai do loop
        else: #se não existir na database
            print("Utilizador não encontrado") #pode tentar outra vez
    password_check() #se o utilizador já existir na database, faz o check à sua password
    print(f"\nBem vindo, {username_input.capitalize()}!") #se a password for correta, imprime isto
    global current_user #agora que temos login feito, vamos mudar o current_user para o utilziador atual e definir que é global
    current_user = username_input #assim as outras funções podem usar isto
    menu() #redireciona para o menu principal

### Define a função de registar utilizadores
def signin():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Registar Novo Utilizador
        {"=" * 50}""")) #imprime cabeçalho
    while True: #loop infinito para garantir que o username tem pelo menos 3 caracteres           
        username_input = input("Utilizador: ")
        if len(username_input) < 3: #se for menor que 3
            print("Insira pelo menos 3 caracteres") #avisa que tem que ser maior que 3
        else: #se for mais que 3
            break #sai do loop
    if username_input not in database: #se o user não existir na database
        password_get() #vamos definir uma password nesta função
        database[username_input] = {
            'password': hashed_password,
            'role':'user'
            } #depois de definir, vamos adicionar esse user, password e role à database
        ### Todos os novos utilizadores são sempre users e não admins
        print(f"\nLogin para o utilizador '{username_input}' criado com sucesso!") #mensagem de sucesso
        input("\nClique enter para voltar ao menu anterior") #espero por um input
        if current_user is None: #se não estiver ninguém com login, é um user novo, por isso:
            login() #vai para o login
        else: #se já estiver com login, é porque tem que ser admin, por isso:
            administration() #manda para o menu 7
    else: #se o utilizador já existir
        print(f"O utilizador {username_input} já existe")
        input("\nClique enter para voltar ao menu anterior") #espera por input
        if current_user is None: #se não estiver ninguém com login, é um user novo, por isso:
            mainHeader() #manda para o menu inicial
        else: #se já estiver com login, é porque tem que ser admin, por isso:
            administration() #manda para o menu 7

### Define a função de remover utilizadores
def removeUser():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Remover Utilizador
        {"=" * 50}""")) #imprime cabeçalho
    while True: #loop infinito para garantir que o user existe
        username_input = input("Utilizador a remover: ")
        if username_input == "": #se clicar enter
           exit() #sai do programa
        elif username_input == current_user: #se o utilizador atual se quiser remover a ele próprio
            print("Não pode eliminar o utilizador atual") #imprime mensagem a dizer que não permite
        elif username_input in database: #se o utilizador existir na database
            while True: #loop infinito para garantir que quer mesmo apagar
                try:
                    remove_confirm = input(dedent(f"""
                    Tem a certeza que quer eliminar o utlizador {username_input}?
                    1. Sim
                    2. Não

                    Selecione a opção desejada: """))
                    if int(remove_confirm) == 1: #se escrever "1"
                        database.pop(username_input) #remove o utilizador da base de dados
                        print(f"\nUtilizador '{username_input}' removido com sucesso!") #mensagem de sucesso
                        input("\nClique enter para voltar ao menu anterior") #espera por input
                        administration() #manda para o menu 7
                    elif int(remove_confirm) == 2: #se escrever "2"
                        administration() #manda para o menu 7
                    else: #se outro número qualquer
                        print("Insira apenas opções entre 1 e 2") #avisa o utilizador das opções permitidas
                except ValueError: #se ValueError
                    print("Insira apenas opções entre 1 e 2") #avisa o utilizador das opções permitidas             
        else: #se o utilizador não existir
            print("Utilizador não encontrado") #avisa o utilizador e ele tenta de novo

### Define a função alterar password de outros utilizadores (só admins)
def changePasswordAdmin():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Alteração de Password
        {"=" * 50}"""))
    while True:
        username_input = input("Alterar password para o utilizador: ") #pede para escolher o utilizador
        if username_input == "": #se clicar enter
            administration() #manda para o menu 7
        elif username_input in database: #se o utilizador existir na database
            break #sai do loop e continua a função
        else: #se não existir na database
            print("Utilizador não encontrado") #avisa o utilizador e tenta de novo
    print("*** Nova Password ***")
    password_get() #pede uma nova password, com os requisitos
    database[username_input]['password'] = hashed_password #altera a password do utilizador desejado
    print(f"\nA password do utilizador '{username_input}' foi atualizada com sucesso!") #mensagem de sucesso
    input("\nClique enter para voltar ao menu anterior") #aguarda input
    administration() #manda para o menu 7

### Define a função alterar password do utilizador atual
def changePassword():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Alteração de Password
        {"=" * 50}"""))
    print("*** Password Atual ***")
    password_check() #pede a password atual, para confirmar que o utilizar a sabe
    print("*** Nova Password ***")
    password_get() #pede uma nova password, com os requisitos
    database[current_user]['password'] = hashed_password #altera a password do utilizador atual
    print(f"\nA sua password foi atualizada com sucesso!") #mensagem de sucesso
    input("\nClique enter para voltar ao menu anterior") #aguarda input
    menu() #volta ao menu principal

### Define a função alterar as permissões dos utilizadores
def changeRole():
    print("\033c", end="") #faz clear ao terminal
    print(dedent(f"""
        {"=" * 50}
        Alteração de Permissões
        {"=" * 50}"""))
    while True:
        username_input = input("Alterar permissões para o utilizador: ")
        if username_input == "": #se clicar enter
            administration() #manda para o menu 7
        elif username_input in database: #se utilizador existir na database
            if username_input == current_user: #confirmar que o utilizador não pode mudar as suas próprias permissões
                print("Não pode alterar as permissões do utilizador atual")
            else:
                break #sai do loop e continua a função
        else: #se não existit na database
            print("Utilizador não encontrado") #avisa o utilizador e tenta novamente
    current_role = database[username_input]['role'] #vai buscar as permissões atuais do utilizador desejado
    if current_role == 'admin': #se for admin
        new_role = 'user' #passa para user
    else: #se for user
        new_role = 'admin' #passa para admin
    print(dedent(f"""
        *** Permissões Atuais ***
        Utilizador: {username_input}
        Permissões: {current_role}\n
        1. Alterar permissões ({current_role} para {new_role})
        2. Manter permissões ({current_role})
        """)) #imprime as opções, incluindo as permissões atuais e futuras
    while True: #loop infinito para escolher a opção
        try:
            role_option = input("Selecione a opção desejada: ")
            if int(role_option) == 1: #se escrever "1"
                database[username_input]['role'] = new_role #altera as permissões do utilizador em questão
                print(f"\nAs permissões do utilizador '{username_input}' foram alteradas com sucesso!")
                input("\nClique enter para voltar ao menu anterior")
                break
            elif int(role_option) == 2: #se escrever "2"
                print(f"As permissões do utilizador '{username_input}' foram mantidas!")
                input("\nClique enter para voltar ao menu anterior")
                break #não altera nada e sai do loop
            else: #se escrever outro número
                print("Insira apenas opções entre 1 e 2") #avisa o utilizador das opções permitidas
        except ValueError: #se ValueError
            print("Insira apenas opções entre 1 e 2") #avisa o utilizador das opções permitidas
    administration() #no fim, retorna ao menu 7

### Define a função para confirmar que a password de um utilizador novo é segura
def password_get():
    global hashed_password #torna a variável global, para ser usada fora da função
    while True: #loop infinito para confirmar que a password é segura
            password = getpass.getpass() #pede uma password ao utilizador
            if len(password) < 8: #confirma que tem mais de 8 caracteres
                print("A password tem que ter um mínimo de 8 caracteres")
            else: #se tiver mais de 8
                lowercase_check = False #iniciamos todas as variaveis de check como falsas
                uppercase_check = False
                numbers_check = False
                special_check = False
                for char in password: #for loop para ir letra a letra da password inserida e procurar por
                    if char in lowercase: #se tem letras minúsculas
                        lowercase_check = True #se sim, passas para True
                    elif char in uppercase: #se tem letras maiúsculas
                        uppercase_check = True #se sim, passas para True
                    elif char in numbers: #se tem digitos
                        numbers_check = True #se sim, passas para True
                    elif char in special: #se tem caracteres especiais
                        special_check = True #se sim, passas para True
                if all([lowercase_check, uppercase_check, numbers_check, special_check]): #todos os checks forem True
                    break #sai do loop e continua a função
                else: #se pelo menos 1 não for True
                    print(dedent(f"""
                        *** Requisitos de Password ***
                        A password deve conter letras minúsculas, maiúsculas, números e caracteres especias ({special})
                        """)) #avisa o utilizador dos requisitos
    password = password.encode() #codificar a password para bytes (necessário para a função de encriptação)
    sha256 = hashlib.sha256() #escolhemos o nosso método de encriptação
    sha256.update(password) #encriptamos a nossa password
    hashed_password = sha256.hexdigest() #passamos a nossa password encriptada para uma representação hexadecimal, para guarda-la

### Define a função para confirmar que a password é correta
def password_check():
    max_attempts = 3 #definimos o número máximo de tentativas de password
    attempts = 0 #começamos com zero tentativas
    while attempts < max_attempts: #enquanto o número de tentativas for inferior a 3
        password_input = getpass.getpass().encode() #pedir password, e codifica-la para bytes
        sha256 = hashlib.sha256() #escolhemos o nosso método de encriptação
        sha256.update(password_input) #encriptamos a password dada
        hashed_input_password = sha256.hexdigest() #passamos a password dada para uma representação hexadecimal
        if database[username_input]['password'] == hashed_input_password: #comparamos com a password na database
            break #se for igual, login com sucesso, sai do loop
        else: #se falhar
            attempts += 1 #acrescentamos 1 às tentativas
            if attempts < max_attempts: #enquanto o número de tentativas for inferior a 3
                print(dedent(f"""
                    {"=" * 50}
                    Password incorreta
                    Tentativas restantes: {max_attempts - attempts}
                    {"=" * 50}
                    """)) #mostramos as tentativas restantes
            else: #quando passar das 3 tentativas
                print("Atingiu o número máximo de tentativas")  #avisamos que esgotou as tentativas
                while True: #loop infinito até que o user clique enter
                    try:
                        exit_input = input("Clique enter para sair")
                        if exit_input == "": #se clicar enter
                            exit() #sai do programa
                        else: #senão
                            print("Atingiu o número máximo de tentativas") #volta ao início do loop até que clique enter
                    except ValueError: #se ValueError
                        print("Atingiu o número máximo de tentativas") #volta ao início do loop até que clique enter

### Define a função para as ferramentas de IP
### Como cada uma das ferramentas é apenas umas linhas de código, foi mais simples juntar tudo
def tool(option): #como aqui mandamos sempre a função e uma opção. Podemos definir ifs dentro da função, tendo em conta a opção que o utilizador escolher
    print("\033c", end="") #faz clear ao terminal
    if option == 1: #se a opção trazida for "1"
        toolHeader() #cabeçalho da ferramenta
        while True: #loop infinito até que o IP seja válido
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP))) #transforma o IP decimal em binário (string)
                resultHeader() #cabeçalho de resultado
                print(f"IP em formato binário: {ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}") #divido os 32 digitos da string em 4 octetos
                print("=" * 50, "\n")
                submenu() #aparece o submenu
            except ValueError: #se não for válido, o módulo ipaddress manda ValueError
                print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
    elif option == 2: #se a opção trazida for "1"
        toolHeader() #cabeçalho da ferramenta
        while True: #loop infinito até que o IP seja válido
            try:
                binaryIP = input("Insira um endereço de IPv4 em formato binário: ")
                binaryIP = binaryIP.replace(".", "") #permitimos IP binário com ou sem pontos a dividir os octetos
                binaryIP = int(binaryIP, 2) #transformamos esta string num número inteiro de base 2
                ip = ipaddress.IPv4Address(binaryIP) #transformamos o IP binário em decimal
                resultHeader() #cabeçalho de resultado
                print(f"IP em formato decimal: {ip}")
                print("=" * 50, "\n")
                submenu() #aparece o submenu
            except ValueError:
                print(f"Insira um IPv4 válido (Ex.: '{defaultBinaryIP()}')")
    elif option == 3: #se a opção trazida for "1"
        toolHeader() #cabeçalho da ferramenta
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
                    resultHeader() #cabeçalho de resultado
                    print(dedent(f"""\
                    Máscara de Rede Adequeada: {network.netmask}
                    CIDR adequado: /{cidr}
                    Número de IPs disponíveis: {network.num_addresses - 2}
                    IP da rede: {network.network_address}
                    Primero IP Disponível: {ipaddress.IPv4Network(network)[1]}
                    Último IP Disponível: {ipaddress.IPv4Network(network)[-2]}
                    IP de Broadcast: {network.broadcast_address}"""))
                    print("=" * 50, "\n")
                    submenu() #aparece o submenu
                except (ValueError, UnboundLocalError):
                    print("Insira um IP de rede válido (Ex:. 10.0.0.0)")
    elif option == 4: #se a opção trazida for "1"
        toolHeader() #cabeçalho da ferramenta
        while True:
            try:
                ip = input("Insira um endereço de IPv4: ")
                if ipaddress.IPv4Address(ip).is_private is True:
                    resultHeader() #cabeçalho de resultado
                    print(f"O IP '{ip}' é um IP Privado")
                    print("=" * 50, "\n")
                    submenu()
                else:
                    resultHeader()
                    print(f"O IP '{ip}' é um IP Público")
                    print("=" * 50, "\n")
                    submenu() #aparece o submenu
            except ValueError:
                print(f"Insira um IPv4 válido (Ex.: '{defaultDecimalIP()}')")
    elif option == 5: #se a opção trazida for "5"
        changePassword() #manda para menu 5
    elif option == 6: #se a opção trazida for "6"
        mainHeader() #manda para menu 6
    elif option == 7: #se a opção trazida for "7"
        administration() #manda para menu 7

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