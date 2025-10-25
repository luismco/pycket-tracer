import ipaddress


while True:
    try:
        ip = input("ip")
        print(ip)
        ipcheck = ipaddress.IPv4Address(ip).is_private
        print(ipcheck)
    except ValueError:
        print("Try again")