from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

# ECC key generation
key = ECC.generate(curve='P-256')

with open('ecc.pub', 'wt') as f:
    f.write(key.public_key().export_key(format='PEM'))
with open('ecc.pem', 'wt') as f:
    f.write(key.export_key(format='PEM'))

# creation digital signature
message = b'ECDSA message for signature'
key = ECC.import_key(open('ecc.pem').read())
h = SHA256.new(message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h)

# verifying the  digital signature
h = SHA256.new(message)
key = ECC.import_key(open('ecc.pub').read())
verifier = DSS.new(key, 'fips-186-3')
try:
    verifier.verify(h, signature)
    print("The message is authentic.")
except ValueError:
    print("The message is not authentic.")
