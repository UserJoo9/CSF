import hashlib
import Details


def new_password(plain_key):
    open(Details.passwordFile, 'w').write(hashlib.sha512(plain_key.encode()).hexdigest())


def init_pass_to_compare(password):
    return hashlib.sha512(password.encode()).hexdigest()


def get_password():
    return open(Details.passwordFile, 'r').read()


if __name__ == '__main__':
    password = "asdasd123"
    new_password(password)
    get_password()