import hashlib
import random
import getpass
import hashlib
from textwrap import dedent
import string

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

while True:
    hosts = input("Insira o número de dispositivos necessários: ")
    if hosts is not int:
          print("Insira apenas números inteiros")
    break

