import hashlib
import Details


def new_password(plain_key, secret_keyword):
    open(Details.passwordFile, 'w').write(hashlib.sha512(plain_key.encode()).hexdigest() + "<>" + hashlib.sha512(secret_keyword.encode()).hexdigest())

def init_pass_to_compare(password):
    return hashlib.sha512(password.encode()).hexdigest()

def get_password():
    return open(Details.passwordFile, 'r').read().split("<>")[0]

def get_keyword():
    return open(Details.passwordFile, 'r').read().split("<>")[1]

if __name__ == '__main__':
    password = "asdasd123"
    new_password(password)
    get_password()