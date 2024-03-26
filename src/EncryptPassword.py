import hashlib
from UserProtection import *


def new_password(plain_key):
    write_to_registry(passwd, hashlib.sha512(plain_key.encode()).hexdigest())


def new_keyword(secret_keyword):
    write_to_registry(keywd, hashlib.sha512(secret_keyword.encode()).hexdigest())


def init_pass_to_compare(password):
    return hashlib.sha512(password.encode()).hexdigest()


def get_password():
    return read_from_registry(passwd)


def get_keyword():
    return read_from_registry(keywd)
