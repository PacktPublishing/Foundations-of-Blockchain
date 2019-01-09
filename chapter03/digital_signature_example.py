import binascii

from Crypto.Hash import SHA256
from ecdsa import SigningKey, VerifyingKey, SECP256k1, keys
from random import randint


class Transaction:

    def __init__(self, public_key):
        self.id = randint(1, 10**5)
        self.signature = None
        self.public_key = public_key

    def verify(self):

        vk = VerifyingKey.from_string(bytes.fromhex(self.public_key), curve=SECP256k1)

        try:
            vk.verify(bytes.fromhex(self.signature), SHA256.new(str(self.id).encode()).digest())

        except keys.BadSignatureError:
            print('invalid transaction signature')
            return False

        return True

    def sign(self, private_key):

        data_to_sign = SHA256.new(str(self.id).encode()).digest()

        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        self.signature = binascii.b2a_hex(sk.sign(data_to_sign)).decode()


class Wallet:
    def __init__(self):

        self.private_key = None
        self.public_key = None

    def generate_key_pair(self):

        sk = SigningKey.generate(curve=SECP256k1)
        self.private_key = binascii.b2a_hex(sk.to_string()).decode()
        self.public_key = binascii.b2a_hex(sk.get_verifying_key().to_string()).decode()


account = Wallet()
account.generate_key_pair()
print("Generated public key: %s" % account.public_key)
print("Generated private key: %s" % account.private_key)

tx = Transaction(account.public_key)
tx.sign(account.private_key)
print("Generated signature: %s" % tx.signature)
tx.verify()

tx.id = '1234'
tx.verify()
