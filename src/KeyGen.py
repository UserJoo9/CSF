from Crypto.PublicKey import RSA
import Details

def generate_keys():
    key = RSA.generate(2048)

    privateKey = key.export_key()
    publicKey = key.publickey().export_key()

    with open(Details.privateKeyPath, 'wb') as f:
        f.write(privateKey)

    with open(Details.publicKeyPath, 'wb') as f:
        f.write(publicKey)

    print('Private key saved to private.pem')
    print('Public key saved to public.pem')
    print('Done')

