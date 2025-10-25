import ipaddress
reguaList = [128,64,32,16,8,4,2,1]

def header():
    print("=" * 50)
    print("Projeto Final Python\nPycket Tracer - Ferramenta de Apoio a Networking\nDiogo Fontes | Luís Oliveira")
    print("=" * 50)

def ferramenta(opcao):
    if opcao == 1:
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("Conversão de IP (Decimal para Binário)")
        print("=" * 50)
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                print(f"{ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                break
            except ValueError:
                print("Insira um IPv4 válido")
    elif opcao == 2:
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("Conversão de IP (Binário para Decimal)")
        print("=" * 50)
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                print(f"{ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                break
            except ValueError:
                print("Insira um IPv4 válido")
    elif opcao == 3:
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("Conversão de IP (Binário para Decimal)")
        print("=" * 50)
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                print(f"{ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                break
            except ValueError:
                print("Insira um IPv4 válido")
    elif opcao == 4:
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("Conversão de IP (Binário para Decimal)")
        print("=" * 50)
        while True:
            try:
                decimalIP = input("Insira um endereço de IPv4 em formato decimal: ")
                ip = ('{:b}'.format(ipaddress.IPv4Address(decimalIP)))
                print(f"{ip[0:9]}.{ip[9:17]}.{ip[17:25]}.{ip[25:33]}")
                break
            except ValueError:
                print("Insira um IPv4 válido")
    elif opcao == 5:
        print("=" * 50)
        print("Pycket Tracer Tools")
        print("Conversão de IP (Binário para Decimal)")
        print("=" * 50)
        print(reguaList)
        while True:
            try:
                opcao5 = input("Clicar 0 para voltar ao menu inicial ou enter para sair: ")
                if opcao5 == "":
                    exit()
                elif int(opcao5) == 0:
                    menu()
                else:
                    print("Insira apenas 0 ou clique enter para sair")
            except ValueError:
                print("Insira apenas 0 ou clique enter para sair")

def menu():
        print("Pycket Tracer Tools")
        print("=" * 50)
        print("1. Conversão de IP (Decimal para Binário)")
        print("2. Conversão de IP (Binário para Decimal)")
        print("3. Cálculo da Máscara de Rede/CIDR")
        print("4. Classicação de IPs (Privado vs Público)")
        print("5. Imprimir a régua de bits")
        print("0. Sair")
        while True:
            try:
                opcao = int(input("Selecione a ferramenta desejada: "))
                if opcao >= 1 and opcao < 6:
                    break
                elif opcao == 0:
                    exit()
                else:
                    print("Insira apenas opções entre 0 e 5")
            except ValueError:
                 print("Insira apenas opções entre 0 e 5")
        if opcao == 1:
            ferramenta(opcao)
        elif opcao == 2:
            ferramenta(opcao)
        elif opcao == 3:
            ferramenta(opcao)
        elif opcao == 4:
            ferramenta(opcao)
        elif opcao == 5:
            ferramenta(opcao)

header()
menu()
