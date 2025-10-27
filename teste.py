import hashlib
import random
import getpass
import hashlib

database = {'luis': {'password': '11a4a60b518bf24989d481468076e5d5982884626aed9faeb35b8576fcd223e1', 'role': 'user'}, 'diogo': {'password': 'c1cc69e61c0f1c7ade8df0f2994e582e7c1f2c57d1ec192a0baf9f96b7739d9d', 'role': 'user'}}
def addUser():
    username = input("Enter username: ")
    password = getpass.getpass().encode()
    sha256 = hashlib.sha256()
    sha256.update(password)
    hashed_password = sha256.hexdigest()
    database[username] = {
    'password': hashed_password,
    'role':'user'
    }
    print(f"Login para user {username} criado com sucesso")

def login():
    while True:
        username_input = input("Username (clique enter para sair): ")
        if username_input == "":
           exit()
        elif username_input in database:
            break
        else:
            print("Username not found, try again")

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        password_input = getpass.getpass().encode()
        sha256 = hashlib.sha256()
        sha256.update(password_input)
        hashed_input_password = sha256.hexdigest()
        if database[username_input]['password'] == hashed_input_password:
            print("login sucesseful")
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print(f"password incorreta. tem mais {max_attempts - attempts} tentativas")
            else:
                print("Demasiadas tentativas")


login()


