#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# Encryption part
message = "plaintext for RSA"

key = RSA.generate(2048)
public = key.publickey()

cipher = PKCS1_OAEP.new(public)
cipher_text = cipher.encrypt(message.encode())
print("Data is encrypted")

# Decryption part
cipher = PKCS1_OAEP.new(key)
message = cipher.decrypt(cipher_text)
print("Decrypted data is : \"{}\"".format(message.decode()))
