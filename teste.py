import ipaddress




def one(x):
    if x == 1:
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                print(f"{ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                break
            except ValueError:
                print("Insira um IPv4 válido")
    elif x == 2:
        print("opcao 2")
        exit()
        

def game():
    while True:
        one(x)
        print("Clique enter para inserir outro IP")
        print("1. Voltar ao menu inicial")
        print("0. Sair")
        while True:
            try:
                opcao = input("Selecione a opção desejada: ")
                if int(opcao) == 1:
                    exit()
                elif int(opcao) == 0:
                    exit()
            except ValueError:
                break

x = input("Escolha uma opcao: ")
x = int(x)
game()