from Crypto.PublicKey import RSA
import base64


key = RSA.generate(2048)

privateKey = key.export_key()
publicKey = key.publickey().export_key()

with open('private.pem', 'wb') as f:
    f.write(privateKey)

with open('public.pem', 'wb') as f:
    f.write(publicKey)

print('Private key saved to private.pem')
print('Public key saved to public.pem')
print('Done')

