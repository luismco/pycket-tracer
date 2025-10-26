import hashlib
import random
import getpass
import hashlib

usernames = []
passwords = []
uid = 2
database = {1: {'Username': 'luis', 'Password(Encrypted)': '11a4a60b518bf24989d481468076e5d5982884626aed9faeb35b8576fcd223e1', 'Role': 'admin'}, 2: {'Username': 'diogo', 'Password(Encrypted)': '11a4a60b518bf24989d481468076e5d5982884626aed9faeb35b8576fcd223e1', 'Role': 'admin'}}
def addUser():
    for x in database.values():
        usernames.append(x['Username'])
    for x in database.values():
        passwords.append(x['Password(Encrypted)'])
    sha256 = hashlib.sha256()
    user = input("Enter username: ")
    global uid
    uid += 1
    passwd = getpass.getpass().encode()
    securepasswd = sha256.update(passwd)
    database[uid] = {
    'Username':user,
    'Password(Encrypted)':sha256.hexdigest(),
    'Role':'user'
    }

addUser()
addUser()

print(usernames)
print(passwords)
print(database)
