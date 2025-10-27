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

current_user = None

letters = string.ascii_letters
numbers = list(range(10))

print(letters)
print(numbers)

password = "Test123!"
print(f"Type of password: {type(password)}")

for char in password:
    print(f"Type of char: {type(char)}, value: {char}")

